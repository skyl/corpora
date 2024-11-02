import typer
from rich import print as rprint

app = typer.Typer(help="Corpus commands")


@app.command()
def init(ctx: typer.Context):
    """Initialize a new corpus - Upload a tarball."""
    # Access the API client from the context
    api_client = ctx.obj["api_client"]
    rprint("Initializing a new corpus...")

    # Example usage (replace with actual API call)
    # response = api_client.create_corpus(...)
    # rprint(response)


@app.command()
def list(ctx: typer.Context):
    """List all corpora."""
    api_client = ctx.obj["api_client"]

    corpora_list = api_client.corpora_api_list_corpora()
    for corpus in corpora_list:
        rprint(f"{corpus.name}")
