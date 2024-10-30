import typer
from rich import print as rprint


app = typer.Typer(help="Corpus commands")


@app.command()
def list():
    """List all corpora."""
    # rprint("Listing all corpora...")
    from corpora_cli.main import corpora_api

    corpora_list = corpora_api.corpora_api_list_corpora()
    for corpus in corpora_list:
        # rprint(dir(corpus))
        # rprint(corpus.json())
        rprint(f"{corpus.name}")
