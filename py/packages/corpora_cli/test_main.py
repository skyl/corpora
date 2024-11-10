import pytest
import typer
from unittest.mock import patch, Mock
from typer.testing import CliRunner
from rich.text import Text

import corpora_client
from corpora_cli.main import get_api_clients, main
from corpora_cli.constants import NO_AUTHENTICATION_MESSAGE
from corpora_cli.auth import AuthError

runner = CliRunner()


# Mock configuration fixture
@pytest.fixture
def mock_config():
    return {
        "server": {"base_url": "https://api.example.com"},
        "auth": {"client_id": "test_client", "client_secret": "test_secret"},
    }


# Mock token fixture
@pytest.fixture
def mock_token():
    return "mocked_token"


@patch("corpora_cli.auth.AuthResolver.resolve_auth")
def test_get_api_clients_successful_authentication(
    mock_resolve_auth, mock_config, mock_token
):
    """Test get_api_clients with successful authentication."""
    # Mock the resolve_auth method to return the token
    mock_resolve_auth.return_value = mock_token

    # Call get_api_clients function with mock configuration
    corpus_api, file_api, split_api, plan_api = get_api_clients(mock_config)

    # Verify configurations and API client creation
    assert corpus_api.api_client.configuration.access_token == mock_token
    assert file_api.api_client.configuration.access_token == mock_token
    assert split_api.api_client.configuration.access_token == mock_token
    assert plan_api.api_client.configuration.access_token == mock_token
    mock_resolve_auth.assert_called_once()


@patch("corpora_cli.main.Console")
@patch("corpora_cli.main.AuthResolver")
def test_get_api_clients_authentication_failure(
    mock_auth_resolver, mock_console, mock_config
):
    """Test get_api_clients with authentication failure."""
    # Mock AuthResolver to raise an AuthError
    mock_auth_resolver.return_value.resolve_auth.side_effect = AuthError("Auth failed")

    with pytest.raises(typer.Exit) as exc_info:
        get_api_clients(mock_config)

    # Verify console error message and exit code
    mock_console.return_value.print.assert_any_call(
        Text("Auth failed", style="bold red")
    )
    mock_console.return_value.print.assert_any_call(
        NO_AUTHENTICATION_MESSAGE, style="yellow"
    )
    # Check if typer.Exit was raised
    assert exc_info.type == typer.Exit


@patch("corpora_cli.main.get_api_clients")
@patch("corpora_cli.main.load_config")
def test_main_callback(mock_load_config, mock_get_api_clients, mock_config, mock_token):
    """Test main callback to ensure context is set up correctly."""
    # Mock configuration and API clients
    mock_load_config.return_value = mock_config
    mock_corpus_api = Mock()
    mock_file_api = Mock()
    mock_split_api = Mock()
    mock_plan_api = Mock()
    mock_get_api_clients.return_value = (
        mock_corpus_api,
        mock_file_api,
        mock_split_api,
        mock_plan_api,
    )
    main(typer.Context)
    mock_get_api_clients.assert_called_once_with(mock_config)
