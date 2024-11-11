from typing import List
from requests import session
import typer
from prompt_toolkit.shortcuts import PromptSession

from corpora_client.models.issue_request_schema import IssueRequestSchema
from corpora_client.models.message_schema import MessageSchema
from corpora_pm.providers.provider_loader import Corpus, load_provider
from corpora_cli.context import ContextObject

app = typer.Typer(help="Interactive issue creation CLI")

session = PromptSession()


@app.command()
def file(ctx: typer.Context, path: str):
    """
    Workon a file in the corpus.
    """
    c: ContextObject = ctx.obj
    c.console.print(f"Working on file: {path}", style="bold blue")

    # show current file content on disk, load the content from the
    # CWD and print it with dim
    c.console.print("Current file content:", style="bold green")
    with open(path, "r") as f:
        c.console.print(f.read(), style="dim")

    # Start with an empty message list
    messages: List[MessageSchema] = []

    # REPL loop
    while True:
        user_input = session.prompt(
            ("What to do?\n" if not messages else "How to revise?\n"),
            multiline=True,
            vi_mode=True,
        )

        if not user_input:
            c.console.print("No input provided. Please try again.", style="yellow")
            continue

        # Add the user's input as a new message
        messages.append(MessageSchema(role="user", text=user_input.strip()))

        # Send the current messages to generate a draft issue
        c.console.print("Generating revision", style="bold blue")
        # revision = c.workon_api.file(
        #     IssueRequestSchema(messages=messages, corpus_id=c.config["id"])
        # )
        # # Display the generated draft issue
        # c.console.print(f"\nDraft Issue:", style="bold green")
        # c.console.print(f"Title: {draft_issue.title}", style="magenta")
        # c.console.print(f"Body:\n{draft_issue.body}", style="dim")

    #     # Confirm if the user wants to post
    #     if typer.confirm("\nPost this issue?"):
    #         issue_tracker = load_provider(
    #             Corpus(url=c.config["url"], id=c.config["id"])
    #         )
    #         resp = issue_tracker.create_issue(
    #             extract_repo_path(c.config["url"]),
    #             draft_issue.title,
    #             draft_issue.body,
    #         )
    #         c.console.print("\nIssue posted!", style="green")
    #         c.console.print(f"URL: {resp.url}", style="magenta")
    #         return
    #     else:
    #         c.console.print(
    #             "\nYou chose not to post the issue. Refine your messages or add new ones.",
    #             style="yellow",
    #         )
    #         messages.append(
    #             MessageSchema(
    #                 role="assistant",
    #                 text=f"{draft_issue.title}\n{draft_issue.body}",
    #             )
    #         )
