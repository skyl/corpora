from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from datetime import datetime


class Issue:
    """
    A class representing a generic issue in an issue tracking system.
    """
    def __init__(
        self,
        id: int,
        title: str,
        body: str,
        created_at: datetime,
        updated_at: datetime,
        state: str,
        labels: Optional[List[str]] = None,
        assignees: Optional[List[str]] = None,
        url: Optional[str] = None
    ):
        self.id = id
        self.title = title
        self.body = body
        self.created_at = created_at
        self.updated_at = updated_at
        self.state = state
        self.labels = labels or []
        self.assignees = assignees or []
        self.url = url


class AbstractIssueTracker(ABC):
    """
    Abstract base class defining the interface for issue tracking systems.
    """

    @abstractmethod
    def list_issues(self, repo: str, state: str = "open") -> List[Issue]:
        """
        List issues for a repository.

        Args:
            repo (str): The repository name in the format "owner/repo".
            state (str): Filter issues by state ("open", "closed", "all").

        Returns:
            List[Issue]: A list of issues.
        """
        pass

    @abstractmethod
    def get_issue(self, repo: str, issue_id: int) -> Issue:
        """
        Retrieve a specific issue by ID.

        Args:
            repo (str): The repository name in the format "owner/repo".
            issue_id (int): The ID of the issue.

        Returns:
            Issue: The retrieved issue.
        """
        pass

    @abstractmethod
    def create_issue(
        self,
        repo: str,
        title: str,
        body: str,
        labels: Optional[List[str]] = None,
        assignees: Optional[List[str]] = None
    ) -> Issue:
        """
        Create a new issue.

        Args:
            repo (str): The repository name in the format "owner/repo".
            title (str): The title of the issue.
            body (str): The body/content of the issue.
            labels (Optional[List[str]]): A list of labels for the issue.
            assignees (Optional[List[str]]): A list of assignees.

        Returns:
            Issue: The created issue.
        """
        pass

    @abstractmethod
    def update_issue(
        self,
        repo: str,
        issue_id: int,
        title: Optional[str] = None,
        body: Optional[str] = None,
        state: Optional[str] = None,
        labels: Optional[List[str]] = None,
        assignees: Optional[List[str]] = None
    ) -> Issue:
        """
        Update an existing issue.

        Args:
            repo (str): The repository name in the format "owner/repo".
            issue_id (int): The ID of the issue.
            title (Optional[str]): The new title of the issue.
            body (Optional[str]): The new body/content of the issue.
            state (Optional[str]): The new state of the issue ("open" or "closed").
            labels (Optional[List[str]]): Updated labels for the issue.
            assignees (Optional[List[str]]): Updated assignees for the issue.

        Returns:
            Issue: The updated issue.
        """
        pass

    @abstractmethod
    def add_comment(self, repo: str, issue_id: int, comment: str) -> None:
        """
        Add a comment to an issue.

        Args:
            repo (str): The repository name in the format "owner/repo".
            issue_id (int): The ID of the issue.
            comment (str): The content of the comment.

        Returns:
            None
        """
        pass

