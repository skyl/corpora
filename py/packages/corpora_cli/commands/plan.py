from urllib.parse import urlparse
import typer

from corpora_cli.context import ContextObject
from corpora_pm.providers.provider_loader import Corpus, load_provider

# provider = load_provider(corpus)


app = typer.Typer(help="Plan commands")


def extract_repo_path(url: str) -> str:
    parsed_url = urlparse(url)
    # Remove leading `/` from the path
    return "/".join(parsed_url.path.strip("/").split("/")[:2])


@app.command()
def issue(ctx: typer.Context, text: str):
    """Get a prospective issue for a given corpus and text."""
    c: ContextObject = ctx.obj
    c.console.print("Generating issue...")
    plan = c.plan_api.get_issue(c.config["id"], text)
    c.console.print(f"Title: {plan.title}")
    c.console.print(f"Body: {plan.body}")
    # c.config has URL and an id ... but a lot more too ... does this work?
    issue_tracker = load_provider(Corpus(url=c.config["url"], id=c.config["id"]))

    # Ask if the user wants to post the issue
    if typer.confirm("Do you want to post this issue?"):
        resp = issue_tracker.create_issue(
            extract_repo_path(c.config["url"]),
            plan.title,
            plan.body,
        )
        c.console.print("Issue posted!", style="green")
        c.console.print(f"URL: {resp.url}", style="magenta")
        c.console.print(f"State: {resp.state}", style="dim")
        c.console.print(f"Assignees: {resp.assignees}", style="dim")
        c.console.print(f"Labels: {resp.labels}", style="dim")
        c.console.print(f"Title: {resp.title}")
        c.console.print(f"Body: {resp.body}")
    else:
        c.console.print("Issue not posted.", style="yellow")

    # console.print all of these
    # resp.assignees, resp.labels, resp.state, resp.url, resp.title, resp.body
