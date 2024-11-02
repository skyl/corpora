import typer
from rich.console import Console
from rich.text import Text
import corpora_client

from corpora_cli.commands import corpus, file
from corpora_cli.config import load_config
from corpora_cli.auth import AuthResolver, AuthError
from corpora_cli.constants import NO_AUTHENTICATION_MESSAGE

app = typer.Typer(help="Corpora CLI: Manage and process your corpora")


def get_api_client(config) -> corpora_client.CorporaApi:
    """
    Initialize and authenticate API client with given config.
    Returns an authenticated CorporaApi instance.
    """
    try:
        # Initialize AuthResolver and authenticate
        auth_resolver = AuthResolver(config)
        auth_token = auth_resolver.resolve_auth()
    except AuthError as e:
        console = Console()
        console.print(Text(str(e), style="bold red"))
        console.print(Text(NO_AUTHENTICATION_MESSAGE, style="bold yellow"))
        raise typer.Exit(code=1)

    # Configure and return the authenticated API client
    client_config = corpora_client.Configuration()
    client_config.host = config["server"]["base_url"]
    client_config.access_token = auth_token
    return corpora_client.CorporaApi(corpora_client.ApiClient(client_config))


@app.callback()
def main(ctx: typer.Context):
    """Main entry point. Sets up configuration and API client."""
    # Load config and pass it to the context
    config = load_config()
    ctx.obj = {"api_client": get_api_client(config), "config": config}


# Register commands with the app
app.add_typer(corpus.app, name="corpus", help="Commands for managing corpora")
app.add_typer(file.app, name="file", help="Commands for file operations")

if __name__ == "__main__":
    app()
