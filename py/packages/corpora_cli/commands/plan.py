from typing import List
import typer
import click
from corpora_ai.llm_interface import ChatCompletionTextMessage
from corpora_client.models.issue_request_schema import IssueRequestSchema
from corpora_client.models.message_schema import MessageSchema
from corpora_pm.providers.provider_loader import Corpus, load_provider
from corpora_cli.context import ContextObject

app = typer.Typer(help="Interactive issue creation CLI")


def extract_repo_path(url: str) -> str:
    return "/".join(url.rstrip("/").split("/")[-2:])


@app.command()
def issue(ctx: typer.Context):
    """
    Interactively create and refine a prospective issue for a given corpus.
    """
    c: ContextObject = ctx.obj
    c.console.print("Entering interactive issue creation...", style="bold blue")

    # Start with an empty message list
    messages: List[MessageSchema] = []

    # REPL loop
    while True:
        # Display the current state of messages
        # # c.console.print("\nCurrent Messages:\n", style="dim")
        # for i, msg in enumerate(messages, start=1):
        #     c.console.print(f"[{msg.role}]\n\n{msg.text}")

        # Allow the user to edit their next input in a text editor
        # user_input = click.edit("")
        # no, just use a typer input
        user_input = typer.prompt(
            "Issue summary" if not messages else "How should we change this issue?"
        )

        if not user_input:
            c.console.print("No input provided. Please try again.", style="yellow")
            continue

        # Add the user's input as a new message
        messages.append(MessageSchema(role="user", text=user_input.strip()))

        # Send the current messages to generate a draft issue
        c.console.print("\nGenerating issue draft...", style="bold blue")
        draft_issue = c.plan_api.get_issue(
            IssueRequestSchema(messages=messages, corpus_id=c.config["id"])
        )
        # Display the generated draft issue
        c.console.print(f"\nDraft Issue:", style="bold green")
        c.console.print(f"Title: {draft_issue.title}", style="magenta")
        c.console.print(f"Body:\n{draft_issue.body}", style="dim")

        # Confirm if the user wants to post
        if typer.confirm("\nPost this issue?"):
            issue_tracker = load_provider(
                Corpus(url=c.config["url"], id=c.config["id"])
            )
            resp = issue_tracker.create_issue(
                extract_repo_path(c.config["url"]),
                draft_issue.title,
                draft_issue.body,
            )
            c.console.print("\nIssue posted!", style="green")
            c.console.print(f"URL: {resp.url}", style="magenta")
            return
        else:
            c.console.print(
                "\nYou chose not to post the issue. Refine your messages or add new ones.",
                style="yellow",
            )
            messages.append(
                MessageSchema(
                    role="assistant",
                    text=f"{draft_issue.title}\n{draft_issue.body}",
                )
            )
