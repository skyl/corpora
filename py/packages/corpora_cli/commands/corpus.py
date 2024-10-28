import typer
from rich import print as rprint
from rich.progress import Progress

app = typer.Typer(help="Corpus commands")


@app.command()
def create(name: str, url: str = None):
    """Create a new corpus."""
    rprint(f"Creating corpus '{name}' with URL: {url}")


@app.command()
def list():
    """List all corpora."""
    rprint("Listing all corpora...")
    with Progress() as progress:
        task = progress.add_task("[green]Fetching corpora...", total=100)
        for _ in range(10):
            progress.update(task, advance=10)
