import json
from pathlib import Path
import typer
from pprint import pformat

from corpora_cli.config import CONFIG_FILE_PATH, save_config
from corpora_cli.constants import CORPUS_EXISTS_MESSAGE
from corpora_cli.context import ContextObject
from corpora_cli.utils.collectors import get_best_collector
from corpora_cli.utils.git import get_file_hash
from corpora_client.exceptions import ApiException

app = typer.Typer(help="Corpus commands")


@app.command()
def init(ctx: typer.Context):
    """Initialize a new corpus - Upload a tarball."""
    c: ContextObject = ctx.obj
    repo_root = Path.cwd()
    config = c.config

    # If config doesn't already exist, save it after successful initialization
    if not Path(CONFIG_FILE_PATH).exists():
        save_config(config)

    c.console.print("Initializing a new corpus...")
    collector = get_best_collector(repo_root, config)
    c.console.print("Gathering files...")
    files = collector.collect_files()
    c.console.print(f"Collected {len(files)} files.")
    tarball = collector.create_tarball(files, repo_root).getvalue()
    c.console.print(f"Tarball created: {len(tarball)} bytes")
    c.console.print("Uploading corpus tarball to server...")

    try:
        res = c.corpus_api.create_corpus(
            name=config["name"],
            url=config["url"],
            tarball=tarball,
        )
        c.console.print(f"{res.name} created!", style="green")

        # Save the returned corpus_id in the config
        config["id"] = res.id
        save_config(config)
        c.console.print(f"Corpus ID saved to {CONFIG_FILE_PATH}", style="blue")

    except ApiException as e:
        if e.status == 409:
            c.console.print(CORPUS_EXISTS_MESSAGE, style="red")
            exit(1)


@app.command()
def sync(ctx: typer.Context):
    """Sync an existing corpus."""
    c: ContextObject = ctx.obj
    repo_root = Path.cwd()

    c.console.print("Syncing corpus...")

    # Ensure the corpus ID exists in the config
    if "id" not in c.config:
        c.console.print(
            "Corpus ID not found in the configuration. Please run 'init' first.",
            style="red",
        )
        raise typer.Exit(code=1)

    corpus_id: str = c.config["id"]
    c.console.print(f"Corpus ID: {corpus_id}")

    # Collect local files and their hashes
    collector = get_best_collector(repo_root, c.config)
    local_files = collector.collect_files()
    local_files_hash_map = {
        file.relative_to(repo_root): get_file_hash(str(file)) for file in local_files
    }
    # TODO: debug flag!
    # c.console.print("Local file hash map:")
    # c.console.print(pformat(local_files_hash_map, width=80))

    # Fetch remote files and their hashes
    remote_files = c.corpus_api.get_file_hashes(corpus_id)
    remote_files_map = {Path(path): hash for path, hash in remote_files.items()}
    # c.console.print("Remote files:")
    # c.console.print(pformat(remote_files_map, width=80))

    # Determine files to update/add and delete
    files_to_update = {
        path: local_hash
        for path, local_hash in local_files_hash_map.items()
        if path not in remote_files_map or local_hash != remote_files_map[path]
    }
    files_to_delete = [
        path for path in remote_files_map if path not in local_files_hash_map
    ]
    c.console.print("Files to update/add:")
    c.console.print(pformat(files_to_update, width=80))

    c.console.print("Files to delete:")
    c.console.print(pformat(files_to_delete, width=80))

    if not files_to_update and not files_to_delete:
        c.console.print("No changes detected. Everything is up-to-date!", style="green")
        return

    # Create tarball for files to update/add
    if files_to_update or files_to_delete:
        c.console.print("Creating tarball for updated/added files... ")
        tarball = collector.create_tarball(
            [repo_root / p for p in files_to_update.keys()], repo_root
        ).getvalue()
        c.console.print(f"Tarball created: {len(tarball)} bytes")

        # TODO: there is a bug in ninja here, I think
        # c.console.print("Files to delete:")
        # c.console.print(pformat(files_to_delete, width=80))
        delete_files = [str(file) for file in files_to_delete] or None
        # c.console.print(f"delete_files: {delete_files}")

        # Upload tarball
        c.console.print("Uploading tarball...")
        c.corpus_api.update_files(
            corpus_id=corpus_id,
            tarball=tarball,
            delete_files=delete_files,
        )
        c.console.print("Update completed!", style="green")


@app.command()
def delete(ctx: typer.Context):
    c: ContextObject = ctx.obj
    corpus_name = c.config["name"]
    c.console.print(f"Deleting corpus: {corpus_name}")
    try:
        c.corpus_api.delete_corpus(corpus_name)
        c.console.print(f"{corpus_name} deleted", style="green")
    except ApiException as e:
        if e.status == 404:
            c.console.print("Corpus not found.", style="red")
            exit(1)
        c.console.print(f"An error occurred. {e}", style="red")


@app.command()
def list(ctx: typer.Context):
    """List all corpora."""
    c: ContextObject = ctx.obj

    corpora_list = c.corpus_api.list_corpora()
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
