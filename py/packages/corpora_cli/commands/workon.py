from typing import List

import typer
from corpora_client.models.corpus_file_chat_schema import CorpusFileChatSchema
from corpora_client.models.message_schema import MessageSchema
from prompt_toolkit.shortcuts import PromptSession

from corpora_cli.context import ContextObject

app = typer.Typer(help="Interactive issue creation CLI")

session = PromptSession()


@app.command()
def file(ctx: typer.Context, path: str):
    """Workon a file in the corpus."""
    c: ContextObject = ctx.obj
    c.console.print(f"Working on file: {path}", style="bold blue")
    ext = path.split(".")[-1]

    # show current file content on disk, load the content from the
    # CWD and print it with dim
    try:
        with open(path) as f:
            current_file_content = f.read() if f else ""
    except FileNotFoundError:
        current_file_content = ""
        open(path, "w").close()  # create the file if it doesn't exist

    c.console.print("Current file content:", style="bold green")
    c.console.print(current_file_content, style="dim")

    # Start with an empty message list
    messages: List[MessageSchema] = []

    if current_file_content:
        messages.append(
            MessageSchema(
                role="user",
                text=f"The original file content was:\n```{ext}\n{current_file_content}```",
            ),
        )

    # REPL loop
    while True:
        user_input = session.prompt(
            ("What to do?\n" if not messages else "How to revise?\n"),
            multiline=True,
            vi_mode=True,
        )

        if not user_input:
            c.console.print(
                "No input provided. Please try again.",
                style="yellow",
            )
            continue

        # Add the user's input as a new message
        messages.append(MessageSchema(role="user", text=user_input.strip()))

        # Send the current messages to generate a draft issue
        c.console.print("Generating revision...", style="bold blue")

        # if file doesn't exist, use empty string
        with open(".corpora/VOICE.md") as f:
            voice = f.read() if f else ""
        with open(".corpora/PURPOSE.md") as f:
            purpose = f.read() if f else ""
        with open(".corpora/STRUCTURE.md") as f:
            structure = f.read() if f else ""
        with open(f".corpora/{ext}/DIRECTIONS.md") as f:
            directions = f.read() if f else ""

        revision = c.workon_api.file(
            CorpusFileChatSchema(
                messages=messages,
                corpus_id=c.config["id"],
                path=path,
                voice=voice,
                purpose=purpose,
                structure=structure,
                directions=directions,
            ),
        )
        c.console.print(f"{revision}", style="dim")
        c.console.print(f"{path}", style="dim magenta")
        messages.append(MessageSchema(role="assistant", text=revision))

        if typer.confirm("Write file?"):
            with open(path, "w") as f:
                f.write(revision)
            c.console.print("File written!", style="green")
            continue
        c.console.print(
            "You chose not to write the file. Give more input to revise.",
            style="magenta",
        )
        continue
