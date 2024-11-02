from gc import collect
from pathlib import Path
import typer

from corpora_cli.context import ContextObject
from corpora_cli.utils.collectors import get_best_collector

app = typer.Typer(help="Corpus commands")


@app.command()
def init(ctx: typer.Context):
    """Initialize a new corpus - Upload a tarball.

    Step-by-Step Ideal CLI Workflow Identify Files in Version Control:

    Use git ls-files to get a list of files tracked by git. This automatically
    respects .gitignore and provides a reliable way to only gather files in
    version control.

    Filter Files Based on corpora.yaml:

    After gathering the list of files, apply filters based on configuration in
    corpora.yaml. For instance, this config file might specify directories or
    file patterns to include/exclude.

    Create an In-Memory Tarball:

    Using Python's tarfile module and io.BytesIO, create a .tar.gz archive in
    memory. This avoids creating temporary files on disk, keeping it efficient
    and straightforward for uploading.

    Upload to the Server:

    Once the tarball is prepared, upload it to the server using the API client.
    You can use requests (or any HTTP client your API client library provides)
    to send the tarball as a file in a multipart/form-data request.
    """
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
    tarball = collector.create_tarball(files, repo_root)
    c.console.print(f"Tarball created: {tarball} - {len(tarball.getvalue())} bytes")
    c.console.print("Uploading corpus tarball to server...")
    # response = c.api_client.corpora_api_create_corpus(
    #     tarball=tarball,
    #     filename="corpus.tar.gz"
    # )


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
