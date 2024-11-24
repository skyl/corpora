from __future__ import annotations

import os
from datetime import datetime
from typing import Any

from corpora_pm.abstract import AbstractIssueTracker, Issue


class GitHubIssueTracker(AbstractIssueTracker):
    """A concrete implementation of AbstractIssueTracker for GitHub."""

    def __init__(
        self,
        token: str = os.environ.get("GITHUB_TOKEN"),
        base_url: str = "https://api.github.com",
    ):
        self.token = token
        self.base_url = base_url

    def _request(
        self,
        method: str,
        endpoint: str,
        data: dict[str, Any] | None = None,
    ) -> Any:
        import requests

        headers = {"Authorization": f"token {self.token}"}
        url = f"{self.base_url}/{endpoint}"
        response = requests.request(
            method,
            url,
            headers=headers,
            json=data,
            timeout=10,
        )
        response.raise_for_status()
        return response.json()

    def list_issues(self, repo: str, state: str = "open") -> list[Issue]:
        endpoint = f"repos/{repo}/issues?state={state}"
        issues_data = self._request("GET", endpoint)
        return [
            Issue(
                id=issue["number"],
                title=issue["title"],
                body=issue["body"],
                created_at=datetime.fromisoformat(issue["created_at"][:-1]),
                updated_at=datetime.fromisoformat(issue["updated_at"][:-1]),
                state=issue["state"],
                labels=[label["name"] for label in issue.get("labels", [])],
                assignees=[
                    assignee["login"] for assignee in issue.get("assignees", [])
                ],
                url=issue["html_url"],
            )
            for issue in issues_data
        ]

    def get_issue(self, repo: str, issue_id: int) -> Issue:
        endpoint = f"repos/{repo}/issues/{issue_id}"
        issue_data = self._request("GET", endpoint)
        return Issue(
            id=issue_data["number"],
            title=issue_data["title"],
            body=issue_data["body"],
            created_at=datetime.fromisoformat(issue_data["created_at"][:-1]),
            updated_at=datetime.fromisoformat(issue_data["updated_at"][:-1]),
            state=issue_data["state"],
            labels=[label["name"] for label in issue_data.get("labels", [])],
            assignees=[
                assignee["login"]
                for assignee in issue_data.get("assignees", [])
            ],
            url=issue_data["html_url"],
        )

    def create_issue(
        self,
        repo: str,
        title: str,
        body: str,
        labels: list[str] | None = None,
        assignees: list[str] | None = None,
    ) -> Issue:
        endpoint = f"repos/{repo}/issues"
        data = {
            "title": title,
            "body": body,
            "labels": labels or [],
            "assignees": assignees or [],
        }
        issue_data = self._request("POST", endpoint, data)
        return self.get_issue(repo, issue_data["number"])

    def update_issue(
        self,
        repo: str,
        issue_id: int,
        title: str | None = None,
        body: str | None = None,
        state: str | None = None,
        labels: list[str] | None = None,
        assignees: list[str] | None = None,
    ) -> Issue:
        endpoint = f"repos/{repo}/issues/{issue_id}"
        data = {
            "title": title,
            "body": body,
            "state": state,
            "labels": labels,
            "assignees": assignees,
        }
        self._request(
            "PATCH",
            endpoint,
            {k: v for k, v in data.items() if v is not None},
        )
        return self.get_issue(repo, issue_id)

    def add_comment(self, repo: str, issue_id: int, comment: str) -> None:
        endpoint = f"repos/{repo}/issues/{issue_id}/comments"
        data = {"body": comment}
        self._request("POST", endpoint, data)
