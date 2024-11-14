from genericpath import exists
import os
import re
import yaml
import typer
from typing import Any, Dict

from corpora_cli.utils.git import get_git_remote_url, get_git_repo_name

CONFIG_FILE_PATH = ".corpora.yaml"
ID_FILE_PATH = ".corpora/.id"
ENV_VAR_PATTERN = re.compile(r"\$\{(\w+)\}")  # Matches ${VAR_NAME}


# TODO: type the config
def load_config() -> Dict[str, Any]:
    """
    Load and parse the .corpora.yaml configuration file, substituting
    any ${VAR_NAME} placeholders with values from environment variables.
    If the config file is missing, infer defaults from Git.
    """
    try:
        # Load YAML config
        with open(CONFIG_FILE_PATH, "r") as file:
            config = yaml.safe_load(file)
        if exists(ID_FILE_PATH):
            with open(ID_FILE_PATH, "r") as file:
                config["id"] = file.read().strip()
    except FileNotFoundError:
        # If config file doesn't exist, fall back to Git
        typer.echo(
            f"Configuration file {CONFIG_FILE_PATH} not found. Using defaults.",
            err=True,
        )
        remote_url = get_git_remote_url()
        repo_name = get_git_repo_name(remote_url)
        if not remote_url or not repo_name:
            typer.echo(
                "Could not infer repository name or URL from Git. Please provide manually.",
                err=True,
            )
            raise typer.Exit(1)
        config = {
            "name": repo_name,
            "url": remote_url,
        }

    # don't need?
    # # Substitute environment variables
    # config = substitute_env_variables(config)

    return config


def save_config(config: Dict[str, Any]) -> None:
    """
    Save the given configuration dictionary to .corpora.yaml.
    """
    with open(CONFIG_FILE_PATH, "w") as file:
        yaml.safe_dump(config, file)


def substitute_env_variables(config: Any) -> Any:
    """
    Recursively substitute ${VAR_NAME} placeholders with environment variables.
    Handles nested dictionaries and lists in the configuration.
    """
    if isinstance(config, dict):
        return {k: substitute_env_variables(v) for k, v in config.items()}
    elif isinstance(config, list):
        return [substitute_env_variables(item) for item in config]
    elif isinstance(config, str):
        # Replace ${VAR_NAME} with its environment value, if available
        return ENV_VAR_PATTERN.sub(lambda match: os.getenv(match.group(1), ""), config)
    return config  # Return non-str types (e.g., int, float) unchanged
