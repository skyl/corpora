import hashlib


def calculate_checksum(content: str) -> str:
    """Calculates MD5 checksum of the content."""
    return hashlib.md5(content.encode("utf-8")).hexdigest()
