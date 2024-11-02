import os
import re
import yaml
import typer
from typing import Any, Dict

CONFIG_FILE_PATH = ".corpora.yaml"
ENV_VAR_PATTERN = re.compile(r"\$\{(\w+)\}")  # Matches ${VAR_NAME}


def load_config() -> Dict[str, Any]:
    """
    Load and parse the .corpora.yaml configuration file, substituting
    any ${VAR_NAME} placeholders with values from environment variables.
    """
    try:
        # Load YAML config
        with open(CONFIG_FILE_PATH, "r") as file:
            config = yaml.safe_load(file)

        # Substitute environment variables
        config = substitute_env_variables(config)

        return config

    except FileNotFoundError:
        typer.echo(f"Configuration file {CONFIG_FILE_PATH} not found.", err=True)
        raise typer.Exit(code=1)
    except yaml.YAMLError as e:
        typer.echo(f"Error parsing YAML configuration: {e}", err=True)
        raise typer.Exit(code=1)


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
