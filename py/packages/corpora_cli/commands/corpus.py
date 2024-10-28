import typer
from rich import print as rprint

app = typer.Typer(help="Corpus commands")


@app.command()
def create(name: str, url: str = None):
    """Create a new corpus."""
    rprint(f"Creating corpus '{name}' with URL: {url}")


@app.command()
def list():
    """List all corpora."""
    rprint("Listing all corpora...")
