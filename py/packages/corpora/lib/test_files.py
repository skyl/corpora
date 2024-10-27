import pytest
from corpora.lib.files import calculate_checksum


@pytest.mark.parametrize(
    "content, expected_checksum",
    [
        ("Hello, world!", "6cd3556deb0da54bca060b4c39479839"),
        ("", "d41d8cd98f00b204e9800998ecf8427e"),  # MD5 of an empty string
        (
            "The quick brown fox jumps over the lazy dog",
            "9e107d9d372bb6826bd81d3542a419d6",
        ),
    ],
)
def test_calculate_checksum(content, expected_checksum):
    """Test that calculate_checksum returns the correct MD5 hash."""
    assert calculate_checksum(content) == expected_checksum
