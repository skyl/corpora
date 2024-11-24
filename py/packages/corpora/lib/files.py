import hashlib
from typing import Union


def compute_checksum(content: Union[bytes, str]) -> str:
    """Compute checksum compatible with Git blob format.

    Accepts either bytes or string input.
    If a string is provided, it is encoded as UTF-8.
    """
    # Convert string to bytes if necessary
    if isinstance(content, str):
        content = content.encode("utf-8")

    size = str(len(content))
    sha = hashlib.sha1(f"blob {size}\0".encode() + content).hexdigest()
    return sha
