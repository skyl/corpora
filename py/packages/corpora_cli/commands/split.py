import typer
from corpora_client.models.split_vector_search_schema import (
    SplitVectorSearchSchema,
)

from corpora_cli.context import ContextObject

app = typer.Typer(help="Split commands")


@app.command()
def search(ctx: typer.Context, text: str, limit: int = 10):
    """Search for splits in the corpus with a given text."""
    if not text:
        raise typer.BadParameter("Missing argument 'TEXT'")
    if limit < 1:
        raise typer.BadParameter("Limit must be greater than 0")
    c: ContextObject = ctx.obj
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
def list(ctx: typer.Context, file_path: str):
    """List all splits for a specific file."""
    c: ContextObject = ctx.obj
    c.console.print(f"Asking for splits... {file_path}")
    fil = c.file_api.get_file_by_path(corpus_id=c.config["id"], path=file_path)
    splits = c.split_api.list_splits_for_file(fil.id)
    for split in splits:
        c.console.print(f"{split.order} {split.content[:100]}", style="dim")
