import hashlib

import pytest

from corpora.lib.files import compute_checksum


def git_blob_checksum(content: bytes) -> str:
    """Helper function to calculate the Git-compatible checksum."""
    size = str(len(content))
    return hashlib.sha1(f"blob {size}\0".encode() + content).hexdigest()


@pytest.mark.parametrize(
    "content, expected_checksum",
    [
        (b"Hello, world!", git_blob_checksum(b"Hello, world!")),
        ("Hello, world!", git_blob_checksum(b"Hello, world!")),
        (b"", git_blob_checksum(b"")),
        ("", git_blob_checksum(b"")),
        (
            b"The quick brown fox jumps over the lazy dog",
            git_blob_checksum(b"The quick brown fox jumps over the lazy dog"),
        ),
        (
            "The quick brown fox jumps over the lazy dog",
            git_blob_checksum(b"The quick brown fox jumps over the lazy dog"),
        ),
    ],
)
def test_compute_checksum(content, expected_checksum):
    """Test that compute_checksum returns the correct Git-compatible checksum for both str and bytes input."""
    assert compute_checksum(content) == expected_checksum
