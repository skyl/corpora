import typer

from corpora_cli.commands import corpus, file
from corpora_cli.config import load_config
from corpora_cli.auth import AuthResolver, AuthError

app = typer.Typer(help="Corpora CLI: Manage and process your corpora")

# Load config for the session
config = load_config()

# Initialize AuthResolver and authenticate
try:
    auth_resolver = AuthResolver(config)
    auth_token = auth_resolver.resolve_auth()
except AuthError as e:
    typer.echo(str(e), err=True)
    raise typer.Exit(code=1)

# Register commands
app.add_typer(corpus.app, name="corpus", help="Commands for managing corpora")
app.add_typer(file.app, name="file", help="Commands for file operations")

if __name__ == "__main__":
    app()
