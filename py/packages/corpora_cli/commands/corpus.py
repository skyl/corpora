from pathlib import Path
import typer

from corpora_cli.constants import CORPUS_EXISTS_MESSAGE
from corpora_cli.context import ContextObject
from corpora_cli.utils.collectors import get_best_collector
from corpora_client.exceptions import ApiException

app = typer.Typer(help="Corpus commands")


@app.command()
def init(ctx: typer.Context):
    """Initialize a new corpus - Upload a tarball."""
    # Access the API client from the context
    c: ContextObject = ctx.obj
    repo_root = Path.cwd()
    # api_client = c.api_client
    # console: Console = ctx.obj["console"]
    c.console.print("Initializing a new corpus...")
    collector = get_best_collector(repo_root, c.config)
    c.console.print("Gathering files...")
    c.console.print(collector, style="dim")
    files = collector.collect_files()
    c.console.print(f"Collected {len(files)} files.")
    # c.console.print(files, style="dim")
    tarball = collector.create_tarball(files, repo_root).getvalue()
    c.console.print(f"Tarball created: {len(tarball)} bytes")
    c.console.print("Uploading corpus tarball to server...")
    try:
        res = c.api_client.corpora_api_create_corpus(
            name=c.config["name"],  # TODO: git repo name?
            url=c.config["url"],  # TODO: get url from git?
            tarball=tarball,
        )
        c.console.print(f"{res.name} created!", style="green")
    except ApiException as e:
        if e.status == 409:
            c.console.print(CORPUS_EXISTS_MESSAGE, style="red")
            exit(1)


@app.command()
def delete(ctx: typer.Context):
    c: ContextObject = ctx.obj
    corpus_name = c.config["name"]
    c.console.print(f"Deleting corpus: {corpus_name}")
    try:
        c.api_client.corpora_api_delete_corpus(corpus_name)
        c.console.print("Corpus deleted.", style="green")
    except ApiException as e:
        if e.status == 404:
            c.console.print("Corpus not found.", style="red")
            exit(1)
        c.console.print(f"An error occurred. {e}", style="red")


@app.command()
def list(ctx: typer.Context):
    """List all corpora."""
    c: ContextObject = ctx.obj

    corpora_list = c.api_client.corpora_api_list_corpora()
    for corpus in corpora_list:
        c.console.print(f"{corpus.name}", style="green")


@app.command()
def print(ctx: typer.Context):
    """This is just a demo command to showcase rich features."""
    c: ContextObject = ctx.obj

    from rich.syntax import Syntax

    # Code
    code = """
    def greet(name):
        return f"Hello, {name}!"
    """
    syntax = Syntax(code, "python", theme="monokai", line_numbers=False)
    c.console.print(syntax)

    # Colors
    c.console.print("Hello [bold magenta]World[/bold magenta]")

    # Table
    from rich.table import Table

    table = Table(title="Sample Table")

    table.add_column("Name", style="cyan", no_wrap=True)
    table.add_column("Age", style="magenta")
    table.add_column("Occupation", justify="right", style="green")

    table.add_row("Alice", "30", "Engineer")
    table.add_row("Bob", "25", "Artist")
    table.add_row("Charlie", "35", "Doctor")

    c.console.print(table)

    # Progress bar
    from rich.progress import track
    import time

    for _ in track(range(10), description="Processing..."):
        time.sleep(0.1)  # Simulate a task

    # Log messages
    c.console.log("This is a log message.")

    # Markdown
    from rich.markdown import Markdown

    markdown = Markdown("# Heading\n\nThis is a **bold** text. ~~nah~~")
    c.console.print(markdown)

    # Panel
    from rich.panel import Panel

    panel = Panel("This is inside a panel.", title="Panel Title", border_style="blue")
    c.console.print(panel)

    # Exceptions
    try:
        1 / 0
    except ZeroDivisionError:
        c.console.print_exception()
