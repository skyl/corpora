import subprocess



def run_command(command: list) -> str:
    """
    Run a command and return its output as a string.
    """
    result = subprocess.run(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True
    )
    return result.stdout.strip()


# see GitCorpusFileCollector
# def get_git_files() -> str:
#     result = run_command(["git", "ls-files"])
#     return result.splitlines()


def get_file_hash(path: str) -> str:
    result = run_command(["git", "hash-object", path])
    return result.strip()


def get_git_remote_url() -> str:
    """
    Retrieve the main remote URL of the current Git repository.
    """
    try:
        result = subprocess.run(
            ["git", "config", "--get", "remote.origin.url"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
        return result.stdout.replace(".git", "").strip()
    except subprocess.CalledProcessError:
        return ""  # Return an empty string if Git command fails


def get_git_repo_name(url: str) -> str:
    """
    Extract the repository name from a Git remote URL.
    """
    if not url:
        return ""
    return url.rstrip("/").split("/")[-1].replace(".git", "")
