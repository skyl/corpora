import typer
from rich import print as rprint

app = typer.Typer(help="File operations within a corpus")


@app.command()
def add(corpus_id: str, path: str):
    """Add a file to a specified corpus."""
    rprint(f"Adding file at {path} to corpus {corpus_id}")


@app.command()
def remove(corpus_id: str, file_id: str):
    """Remove a file from a corpus."""
    rprint(f"Removing file {file_id} from corpus {corpus_id}")
