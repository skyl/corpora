from typing import List
import typer
from prompt_toolkit.shortcuts import PromptSession

from corpora_client.models.issue_request_schema import IssueRequestSchema
from corpora_client.models.message_schema import MessageSchema
from corpora_pm.providers.provider_loader import Corpus, load_provider
from corpora_cli.context import ContextObject

app = typer.Typer(help="Interactive issue creation CLI")


session = PromptSession()


def extract_repo_path(url: str) -> str:
    return "/".join(url.rstrip("/").split("/")[-2:])


def get_file_content_or_create(path: str) -> str:
    try:
        with open(path, "r") as f:
            return f.read()
    except FileNotFoundError:
        with open(path, "w") as f:
            return ""


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
        user_input = session.prompt(
            (
                "Issue summary:\n"
                if not messages
                else "How should we change this issue?\n"
            ),
            multiline=True,
            vi_mode=True,
        )
        c.console.print("Thinking...", style="bold blue")

        if not user_input:
            c.console.print("No input provided. Please try again.", style="yellow")
            continue

        # Add the user's input as a new message
        messages.append(MessageSchema(role="user", text=user_input.strip()))

        # Send the current messages to generate a draft issue
        c.console.print("Generating issue draft...", style="bold blue")

        voice = get_file_content_or_create(".corpora/VOICE.md")
        purpose = get_file_content_or_create(".corpora/PURPOSE.md")
        structure = get_file_content_or_create(".corpora/STRUCTURE.md")
        directions = get_file_content_or_create(".corpora/md/DIRECTIONS.md")

        draft_issue = c.plan_api.get_issue(
            IssueRequestSchema(
                messages=messages,
                corpus_id=c.config["id"],
                voice=voice,
                purpose=purpose,
                structure=structure,
                directions=directions,
            )
        )
        # Display the generated draft issue
        c.console.print(f"Draft Issue:", style="bold green")
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
            c.console.print("Issue posted!", style="green")
            c.console.print(f"URL: {resp.url}", style="magenta")
            return
        else:
            c.console.print(
                "You chose not to post the issue. Refine your messages or add new ones.",
                style="yellow",
            )
            messages.append(
                MessageSchema(
                    role="assistant",
                    text=f"{draft_issue.title}\n{draft_issue.body}",
                )
            )


@app.command()
def update_issue(ctx: typer.Context, issue_number: int):
    """
    Interactively update an existing issue for a given corpus.
    """
    c: ContextObject = ctx.obj
    c.console.print("Fetching existing issue...", style="bold blue")

    issue_tracker = load_provider(Corpus(url=c.config["url"], id=c.config["id"]))
    repo_path = extract_repo_path(c.config["url"])
    existing_issue = issue_tracker.get_issue(repo_path, issue_number)

    # Start with the existing issue state
    messages: List[MessageSchema] = [
        MessageSchema(
            role="user", text=f"Title: {existing_issue.title}\n{existing_issue.body}"
        )
    ]

    c.console.print("Existing Issue:", style="bold green")
    c.console.print(f"Title: {existing_issue.title}", style="magenta")
    c.console.print(f"Body:\n{existing_issue.body}\n", style="dim")

    # REPL loop
    while True:
        user_input = session.prompt(
            (
                "Current issue content:\n"
                if not messages
                else "What changes would you like to make to this issue?\n"
            ),
            multiline=True,
            vi_mode=True,
        )
        c.console.print("Thinking...", style="bold blue")

        if not user_input:
            c.console.print("No input provided. Please try again.", style="yellow")
            continue

        # Add the user's input as a new message
        messages.append(MessageSchema(role="user", text=user_input.strip()))

        # Send the current messages to generate an updated issue draft
        c.console.print("Generating updated issue draft...", style="bold blue")

        voice = get_file_content_or_create(".corpora/VOICE.md")
        purpose = get_file_content_or_create(".corpora/PURPOSE.md")
        structure = get_file_content_or_create(".corpora/STRUCTURE.md")
        directions = get_file_content_or_create(".corpora/md/DIRECTIONS.md")

        updated_issue = c.plan_api.get_issue(
            IssueRequestSchema(
                messages=messages,
                corpus_id=c.config["id"],
                voice=voice,
                purpose=purpose,
                structure=structure,
                directions=directions,
            )
        )
        # Display the updated draft issue
        c.console.print(f"Updated Draft Issue:", style="bold green")
        c.console.print(f"Title: {updated_issue.title}", style="magenta")
        c.console.print(f"Body:\n{updated_issue.body}", style="dim")

        # Confirm if the user wants to update
        if typer.confirm("\nUpdate this issue?"):
            resp = issue_tracker.update_issue(
                repo_path,
                issue_number,
                title=updated_issue.title,
                body=updated_issue.body,
            )
            c.console.print("Issue updated!", style="green")
            c.console.print(f"URL: {resp.url}", style="magenta")
            return
        else:
            c.console.print(
                "You chose not to update the issue. Refine your messages or add new ones.",
                style="yellow",
            )
            messages.append(
                MessageSchema(
                    role="assistant",
                    text=f"{updated_issue.title}\n{updated_issue.body}",
                )
            )
