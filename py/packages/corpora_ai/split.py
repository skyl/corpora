import os

from git import Union
from langchain_text_splitters import (
    PythonCodeTextSplitter,
    MarkdownHeaderTextSplitter,
    CharacterTextSplitter,
)


def get_text_splitter(
    file_name: str,
    chunk_size: int = 5000,  # number of characters
    chunk_overlap: int = 0,  # number of characters
) -> Union[PythonCodeTextSplitter, MarkdownHeaderTextSplitter, CharacterTextSplitter]:
    """
    Returns an appropriate text splitter based on the file extension or name.
    """
    # Mapping specific extensions to splitters
    extension_to_splitter = {
        ".py": PythonCodeTextSplitter,
        ".md": MarkdownHeaderTextSplitter,
        # Add more mappings as needed
    }

    # Extract the extension (if available) and lower-case for consistency
    _, ext = os.path.splitext(file_name)
    ext = ext.lower()

    # Handle files without extensions using a default splitter
    splitter_class = extension_to_splitter.get(ext, None)

    # For files with defined splitters, return the configured splitter instance
    if splitter_class:
        return splitter_class(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    # For text-based formats or unknown extensions, use CharacterTextSplitter with `\n\n`
    return CharacterTextSplitter(
        separator="\n\n", chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
