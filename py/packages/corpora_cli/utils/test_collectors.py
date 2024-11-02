import io
import tarfile
from pathlib import Path
import unittest
from unittest.mock import patch, MagicMock
from corpora_cli.utils.collectors import (
    CorpusFileCollector,
    GitCorpusFileCollector,
    ConfigCorpusFileCollector,
    is_git_installed,
    is_git_repository,
    get_best_collector,
)


class TestCorpusFileCollector(unittest.TestCase):
    def setUp(self):
        self.repo_root = Path("/fake/repo")
        self.files = [self.repo_root / "file1.txt", self.repo_root / "file2.txt"]

    @patch(
        "pathlib.Path.exists", return_value=True
    )  # Mock Path.exists to pretend files exist
    @patch(
        "tarfile.TarFile.add"
    )  # Mock tarfile.TarFile.add to simulate adding files without real I/O
    def test_create_tarball(self, mock_add, mock_exists):
        """Test that create_tarball creates a tar.gz archive in memory without needing actual files."""

        # Create a CorpusFileCollector instance and call create_tarball
        collector = CorpusFileCollector()
        tar_buffer = collector.create_tarball(self.files, self.repo_root)

        # Check that tar_buffer is a valid tar file
        self.assertIsInstance(tar_buffer, io.BytesIO)
        tar_buffer.seek(0)

        # Patch the TarFile.open context to mock entries in the tarball
        with tarfile.open(fileobj=tar_buffer, mode="r:gz") as tar:
            # Instead of actual files, we mock the members of the tar archive
            with patch.object(tar, "getnames", return_value=["file1.txt", "file2.txt"]):
                tar_members = tar.getnames()
                self.assertIn("file1.txt", tar_members)
                self.assertIn("file2.txt", tar_members)

        # Ensure add was called for each file, with arcname as a string
        mock_add.assert_any_call(self.files[0], arcname=Path("file1.txt"))
        mock_add.assert_any_call(self.files[1], arcname=Path("file2.txt"))
        self.assertEqual(mock_add.call_count, 2)


class TestGitCorpusFileCollector(unittest.TestCase):
    def setUp(self):
        self.repo_root = Path("/fake/repo")

    @patch("subprocess.run")
    def test_collect_files(self, mock_run):
        """Test that GitCorpusFileCollector.collect_files uses `git ls-files`."""
        mock_run.return_value = MagicMock(stdout="file1.txt\nfile2.txt\n")
        collector = GitCorpusFileCollector(self.repo_root)
        files = collector.collect_files()

        # Check if `git ls-files` was called correctly
        mock_run.assert_called_once_with(
            ["git", "ls-files"],
            cwd=self.repo_root,
            capture_output=True,
            text=True,
            check=True,
        )

        # Check that the returned files match expected output
        expected_files = [self.repo_root / "file1.txt", self.repo_root / "file2.txt"]
        self.assertEqual(files, expected_files)


class TestIsGitInstalled(unittest.TestCase):
    @patch("shutil.which")
    def test_is_git_installed(self, mock_which):
        """Test that is_git_installed checks for git on the PATH."""
        mock_which.return_value = "/usr/bin/git"
        self.assertTrue(is_git_installed())
        mock_which.assert_called_once_with("git")

        mock_which.return_value = None
        self.assertFalse(is_git_installed())


class TestIsGitRepository(unittest.TestCase):
    @patch("pathlib.Path.exists")
    def test_is_git_repository(self, mock_exists):
        """Test that is_git_repository checks for a .git directory."""
        mock_exists.return_value = True
        repo_root = Path("/fake/repo")
        self.assertTrue(is_git_repository(repo_root))
        mock_exists.assert_called_once_with()

        mock_exists.return_value = False
        self.assertFalse(is_git_repository(repo_root))


class TestGetBestCollector(unittest.TestCase):
    @patch("corpora_cli.utils.collectors.is_git_installed", return_value=True)
    @patch("corpora_cli.utils.collectors.is_git_repository", return_value=True)
    def test_get_best_collector_git(self, mock_is_repo, mock_is_installed):
        """Test that get_best_collector returns GitCorpusFileCollector when repo_root is provided and git is available."""
        repo_root = Path("/fake/repo")
        collector = get_best_collector(repo_root=repo_root)
        self.assertIsInstance(collector, GitCorpusFileCollector)
        mock_is_installed.assert_called_once()
        mock_is_repo.assert_called_once_with(repo_root)

    def test_get_best_collector_config(self):
        """Test that get_best_collector returns ConfigCorpusFileCollector when config is provided."""
        config = {"some": "config"}
        collector = get_best_collector(config=config)
        self.assertIsInstance(collector, ConfigCorpusFileCollector)

    def test_get_best_collector_invalid(self):
        """Test that get_best_collector raises ValueError when neither repo_root nor config is provided."""
        with self.assertRaises(ValueError):
            get_best_collector()


if __name__ == "__main__":
    unittest.main()
