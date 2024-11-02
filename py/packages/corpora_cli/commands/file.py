import typer

from corpora_cli.context import ContextObject

app = typer.Typer(help="File operations within a corpus")


@app.command()
def add(ctx: typer.Context, corpus_id: str, path: str):
    """Add a file to a specified corpus."""
    c: ContextObject = ctx.obj
    c.console.print(f"Adding file at {path} to corpus {corpus_id}", style="green")


@app.command()
def remove(ctx: typer.Context, corpus_id: str, file_id: str):
    """Remove a file from a corpus."""
    c: ContextObject = ctx.obj
    c.console.print(f"Removing file {file_id} from corpus {corpus_id}")
