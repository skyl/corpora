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
@patch("yaml.safe_load")
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
def test_load_config_missing_file(mock_file_open):
    """Test load_config falls back to defaults when file is missing."""
    mock_file_open.side_effect = FileNotFoundError

    # Mock Git defaults
    with patch(
        "corpora_cli.config.get_git_remote_url",
        return_value="https://example.com/test-repo",
    ):
        with patch("corpora_cli.config.get_git_repo_name", return_value="test-repo"):
            config = load_config()

    # Assert defaults are set
    assert config["name"] == "test-repo"
    assert config["url"] == "https://example.com/test-repo"


@patch("builtins.open", new_callable=mock_open)
def test_load_config_invalid_yaml(mock_file_open):
    """Test load_config raises a yaml.YAMLError on YAML parsing error."""
    # Simulate invalid YAML content in the file
    mock_file_open.return_value.__enter__.return_value = "invalid: yaml: content"

    # Mock yaml.safe_load to raise a YAMLError
    with patch("yaml.safe_load", side_effect=yaml.YAMLError("YAML parsing error")):
        with pytest.raises(yaml.YAMLError, match="YAML parsing error"):
            load_config()

    # Ensure that the file was attempted to be opened
    mock_file_open.assert_called_once_with(".corpora.yaml", "r")


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
