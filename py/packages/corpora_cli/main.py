import typer

from .commands import corpus, file
from .config import load_config
from .auth import authenticate

app = typer.Typer(help="Corpora CLI: Manage and process your corpora")

# Load config and authenticate globally for the CLI session
config = load_config()
auth_token = authenticate(config["auth"]["client_id"], config["auth"]["client_secret"])

# Register commands
app.add_typer(corpus.app, name="corpus", help="Commands for managing corpora")
app.add_typer(file.app, name="file", help="Commands for file operations")

if __name__ == "__main__":
    app()
