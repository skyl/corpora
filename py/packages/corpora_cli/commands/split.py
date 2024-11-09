import typer

from corpora_cli.context import ContextObject
from corpora_client.models.split_vector_search_schema import SplitVectorSearchSchema

app = typer.Typer(help="Split commands")


@app.command()
def search(ctx: typer.Context, text: str, limit: int = 10):
    """Search for splits."""
    if not text:
        raise typer.BadParameter("Missing argument 'TEXT'")
    if limit < 1:
        raise typer.BadParameter("Limit must be greater than 0")
    print(f"FFFUCK {text}, {limit}")
    c: ContextObject = ctx.obj
    # c.corpus_api.get_corpus()
    c.console.print("Searching for splits...")
    query = SplitVectorSearchSchema(
        # TODO: how do we really want to identify the corpus?
        corpus_id=c.config["id"],
        text=text,
        limit=limit,
    )
    res = c.split_api.vector_search(query)
    for split in res:
        # c.console.print(f"File ID: {split.file_id}")
        phial = c.file_api.get_file(split.file_id)
        c.console.print(f"File: {phial.path}")
        c.console.print(f"{split.order} {split.content[:100]}", style="dim")
        # c.console.print(phial.content[:100], style="dim")


@app.command()
def ask(ctx: typer.Context, text: str):
    """Ask for splits."""
    c: ContextObject = ctx.obj
    c.console.print("Asking for splits...")
