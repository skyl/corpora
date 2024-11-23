import io
import shutil
import subprocess
import tarfile
from pathlib import Path
from typing import Dict, List, Optional


class CorpusFileCollector:
    """Abstract base class for collecting corpus files.
    Implementations should define how to collect files.
    """

    def collect_files(self) -> List[Path]:
        raise NotImplementedError("Must implement collect_files method")

    def create_tarball(self, files: List[Path], repo_root: Path) -> io.BytesIO:
        """Creates a tar.gz archive in memory for a list of files.
        """
        tar_buffer = io.BytesIO()
        with tarfile.open(fileobj=tar_buffer, mode="w:gz") as tar:
            for file_path in files:
                tar.add(file_path, arcname=file_path.relative_to(repo_root))
        tar_buffer.seek(0)
        return tar_buffer


class GitCorpusFileCollector(CorpusFileCollector):
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root

    def collect_files(self) -> List[Path]:
        """Uses `git ls-files` to collect files tracked by Git."""
        result = subprocess.run(
            ["git", "ls-files"],
            cwd=self.repo_root,
            capture_output=True,
            text=True,
            check=True,
        )
        files = result.stdout.strip().split("\n")
        return [self.repo_root / f for f in files if f]


class ConfigCorpusFileCollector(CorpusFileCollector):
    def __init__(self, config: dict):
        self.config = config

    def collect_files(self) -> List[Path]:
        """Collect files based on `corpora.yaml` configuration."""
        # Placeholder implementation
        raise NotImplementedError("ConfigCorpusFileCollector not yet implemented")


def is_git_installed() -> bool:
    """Check if Git is installed by verifying if `git` is on the PATH."""
    return shutil.which("git") is not None


def is_git_repository(repo_root: Path) -> bool:
    """Check if the provided path is a valid Git repository."""
    return (repo_root / ".git").exists()


def get_best_collector(
    repo_root: Optional[Path] = None, config: Optional[Dict] = None,
) -> "CorpusFileCollector":
    """Factory function to get the most appropriate file collector based on provided arguments.

    Args:
        repo_root (Optional[Path]): The root path of the repository (if any).
        config (Optional[Dict]): Configuration data from corpora.yaml (if any).

    Returns:
        CorpusFileCollector: An instance of the best collector for the situation.

    Raises:
        ValueError: If neither repo_root nor config is suitable for any collector.

    """
    if repo_root and is_git_installed() and is_git_repository(repo_root):
        return GitCorpusFileCollector(repo_root)
    if config:
        return ConfigCorpusFileCollector(config)

    raise ValueError(
        "Unable to determine an appropriate file collector. Please provide a valid `repo_root` for a Git repository or a `config`.",
    )
