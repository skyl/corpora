import os
import yaml
import pytest
from unittest.mock import patch, mock_open
import typer

from corpora_cli.config import load_config, substitute_env_variables


@pytest.fixture
def yaml_content():
    """Sample YAML content for testing."""
    return """
    server:
      base_url: "http://localhost:8000"
    auth:
      client_id: "${CORPORA_CLIENT_ID}"
      client_secret: "${CORPORA_CLIENT_SECRET}"
      optional_auth: "${OPTIONAL_AUTH}"
    corpora:
      - name: "default"
        globs:
          - "**/*.*"
    """


@pytest.fixture
def mocked_env():
    """Mocked environment variables for testing."""
    with patch.dict(
        os.environ,
        {
            "CORPORA_CLIENT_ID": "test_client_id",
            "CORPORA_CLIENT_SECRET": "test_client_secret",
            "OPTIONAL_AUTH": "optional_auth_value",
        },
    ):
        yield


@patch("builtins.open", new_callable=mock_open)
@patch("config.yaml.safe_load")
def test_load_config_success(mock_yaml_load, mock_file_open, yaml_content, mocked_env):
    """Test load_config with successful loading and env substitution."""
    # Set up mock for yaml.safe_load to return the parsed YAML structure
    mock_yaml_load.return_value = {
        "server": {"base_url": "http://localhost:8000"},
        "auth": {
            "client_id": "${CORPORA_CLIENT_ID}",
            "client_secret": "${CORPORA_CLIENT_SECRET}",
            "optional_auth": "${OPTIONAL_AUTH}",
        },
        "corpora": [{"name": "default", "globs": ["**/*.*"]}],
    }

    # Test loading and substitution
    config = load_config()

    # Check substituted environment variables
    assert config["auth"]["client_id"] == "test_client_id"
    assert config["auth"]["client_secret"] == "test_client_secret"
    assert config["auth"]["optional_auth"] == "optional_auth_value"
    assert config["server"]["base_url"] == "http://localhost:8000"


@patch("builtins.open", new_callable=mock_open)
@patch("config.yaml.safe_load")
def test_load_config_missing_file(mock_yaml_load, mock_file_open):
    """Test load_config raises typer.Exit when file is missing."""
    mock_file_open.side_effect = FileNotFoundError

    # Expect typer.Exit instead of SystemExit
    with pytest.raises(typer.Exit):
        load_config()


@patch("builtins.open", new_callable=mock_open)
def test_load_config_invalid_yaml(mock_file_open):
    """Test load_config raises typer.Exit on YAML parsing error."""
    # Set up a file-like object for invalid YAML content
    mock_file_open.return_value.__enter__.return_value = "invalid: yaml: content"

    with patch(
        "config.yaml.safe_load", side_effect=yaml.YAMLError("YAML parsing error")
    ):
        with pytest.raises(typer.Exit):
            load_config()


def test_substitute_env_variables(mocked_env):
    """Test substitute_env_variables function for various input cases."""
    config = {
        "auth": {
            "client_id": "${CORPORA_CLIENT_ID}",
            "client_secret": "${CORPORA_CLIENT_SECRET}",
            "nonexistent_var": "${NON_EXISTENT_VAR}",
        },
        "server": {"base_url": "http://localhost:8000"},
    }
    substituted_config = substitute_env_variables(config)

    assert substituted_config["auth"]["client_id"] == "test_client_id"
    assert substituted_config["auth"]["client_secret"] == "test_client_secret"
    assert (
        substituted_config["auth"]["nonexistent_var"] == ""
    )  # Non-existent vars default to ""
    assert substituted_config["server"]["base_url"] == "http://localhost:8000"
