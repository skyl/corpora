import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from corpora_pm.providers.github.pm import GitHubIssueTracker
from corpora_pm.abstract import Issue


class TestGitHubIssueTracker(unittest.TestCase):
    def setUp(self):
        self.token = "fake_token"
        self.repo = "fake_repo"
        self.issue_id = 1
        self.tracker = GitHubIssueTracker(token=self.token)

    @patch("requests.request")
    def test_list_issues(self, mock_request):
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {
                "number": 1,
                "title": "Issue 1",
                "body": "Body of issue 1",
                "created_at": "2023-01-01T00:00:00Z",
                "updated_at": "2023-01-02T00:00:00Z",
                "state": "open",
                "labels": [{"name": "bug"}],
                "assignees": [{"login": "user1"}],
                "html_url": "https://github.com/fake_repo/issues/1",
            }
        ]
        mock_request.return_value = mock_response

        issues = self.tracker.list_issues(self.repo)
        self.assertEqual(len(issues), 1)
        self.assertIsInstance(issues[0], Issue)
        self.assertEqual(issues[0].id, 1)
        self.assertEqual(issues[0].title, "Issue 1")

    @patch("requests.request")
    def test_get_issue(self, mock_request):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "number": 1,
            "title": "Issue 1",
            "body": "Body of issue 1",
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-02T00:00:00Z",
            "state": "open",
            "labels": [{"name": "bug"}],
            "assignees": [{"login": "user1"}],
            "html_url": "https://github.com/fake_repo/issues/1",
        }
        mock_request.return_value = mock_response

        issue = self.tracker.get_issue(self.repo, self.issue_id)
        self.assertIsInstance(issue, Issue)
        self.assertEqual(issue.id, 1)
        self.assertEqual(issue.title, "Issue 1")

    @patch("requests.request")
    def test_create_issue(self, mock_request):
        mock_response = MagicMock()
        mock_response.json.return_value = {"number": 1}
        mock_request.return_value = mock_response

        with patch.object(
            self.tracker,
            "get_issue",
            return_value=Issue(
                id=1,
                title="New Issue",
                body="Body of new issue",
                created_at=datetime.now(),
                updated_at=datetime.now(),
                state="open",
                labels=[],
                assignees=[],
                url="https://github.com/fake_repo/issues/1",
            ),
        ):
            issue = self.tracker.create_issue(
                self.repo, "New Issue", "Body of new issue"
            )
            self.assertIsInstance(issue, Issue)
            self.assertEqual(issue.id, 1)
            self.assertEqual(issue.title, "New Issue")

    @patch("requests.request")
    def test_update_issue(self, mock_request):
        mock_response = MagicMock()
        mock_response.json.return_value = {"number": 1}
        mock_request.return_value = mock_response

        with patch.object(
            self.tracker,
            "get_issue",
            return_value=Issue(
                id=1,
                title="Updated Issue",
                body="Updated body of issue",
                created_at=datetime.now(),
                updated_at=datetime.now(),
                state="open",
                labels=[],
                assignees=[],
                url="https://github.com/fake_repo/issues/1",
            ),
        ):
            issue = self.tracker.update_issue(
                self.repo,
                self.issue_id,
                title="Updated Issue",
                body="Updated body of issue",
            )
            self.assertIsInstance(issue, Issue)
            self.assertEqual(issue.id, 1)
            self.assertEqual(issue.title, "Updated Issue")

    @patch("requests.request")
    def test_add_comment(self, mock_request):
        mock_response = MagicMock()
        mock_request.return_value = mock_response

        self.tracker.add_comment(self.repo, self.issue_id, "This is a comment")
        mock_request.assert_called_once_with(
            "POST",
            f"https://api.github.com/repos/{self.repo}/issues/{self.issue_id}/comments",
            headers={"Authorization": f"token {self.token}"},
            json={"body": "This is a comment"},
        )


if __name__ == "__main__":
    unittest.main()
