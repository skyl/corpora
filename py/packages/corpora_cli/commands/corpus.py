import typer

from corpora_cli.context import ContextObject

app = typer.Typer(help="Corpus commands")


@app.command()
def init(ctx: typer.Context):
    """Initialize a new corpus - Upload a tarball."""
    # Access the API client from the context
    c: ContextObject = ctx.obj
    # api_client = c.api_client
    # console: Console = ctx.obj["console"]
    c.console.print("Initializing a new corpus...")
    # c.api_client.corpora_api_create_corpus()

    # Example usage (replace with actual API call)
    # response = api_client.create_corpus(...)
    # rprint(response)


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
        time.sleep(0.05)  # Simulate a task

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
