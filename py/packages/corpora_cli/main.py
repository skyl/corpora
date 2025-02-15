#!/usr/bin/env python3

from typing import Tuple

import corpora_client
import typer
from rich.console import Console
from rich.text import Text

from corpora_cli.auth import AuthError, AuthResolver
from corpora_cli.commands import corpus, file, plan, split, workon
from corpora_cli.config import load_config
from corpora_cli.constants import NO_AUTHENTICATION_MESSAGE
from corpora_cli.context import ContextObject

app = typer.Typer(help="Corpora CLI: Manage and process your corpora")


def get_api_clients(
    config,
) -> Tuple[
    corpora_client.CorpusApi,
    corpora_client.FileApi,
    corpora_client.SplitApi,
    corpora_client.PlanApi,
    corpora_client.WorkonApi,
]:
    """Initialize and authenticate API client with given config.
    Returns an authenticated CorporaApi instance.
    """
    try:
        # Initialize AuthResolver and authenticate
        auth_resolver = AuthResolver(config)
        auth_token = auth_resolver.resolve_auth()
    except AuthError as e:
        console = Console()
        console.print(Text(str(e), style="bold red"))
        console.print(NO_AUTHENTICATION_MESSAGE, style="yellow")
        raise typer.Exit(code=1)

    # Configure and return the authenticated API client
    client_config = corpora_client.Configuration()
    # TODO: deploy and default to the main production server?
    client_config.host = config.get("server", {}).get(
        "base_url", "http://corpora-app:8877",
    )
    client_config.access_token = auth_token
    return (
        corpora_client.CorpusApi(corpora_client.ApiClient(client_config)),
        corpora_client.FileApi(corpora_client.ApiClient(client_config)),
        corpora_client.SplitApi(corpora_client.ApiClient(client_config)),
        corpora_client.PlanApi(corpora_client.ApiClient(client_config)),
        corpora_client.WorkonApi(corpora_client.ApiClient(client_config)),
    )


@app.callback()
def main(ctx: typer.Context):
    """Main entry point. Sets up configuration and API client."""
    corpus_api, files_api, split_api, plan_api, workon_api = get_api_clients(
        load_config(),
    )

    config = load_config()
    ctx.obj = ContextObject(
        corpus_api=corpus_api,
        file_api=files_api,
        split_api=split_api,
        plan_api=plan_api,
        workon_api=workon_api,
        config=config,
        console=Console(),
    )


# Register commands with the app
app.add_typer(corpus.app, name="corpus", help="Commands for managing corpora")
app.add_typer(file.app, name="file", help="Commands for file operations")
app.add_typer(split.app, name="split", help="Commands for split operations")
app.add_typer(plan.app, name="plan", help="Commands for plan operations")
app.add_typer(
    workon.app, name="workon", help="Commands for working on files in the corpus",
)

if __name__ == "__main__":
    app()
