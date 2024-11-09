from io import StringIO
from unittest.mock import patch, MagicMock
from typer.testing import CliRunner
from rich.console import Console

from corpora_cli.commands.split import app  # Adjust if the path is different

runner = CliRunner()


@patch("corpora_cli.commands.split.ContextObject")
def test_search_command(mock_context):
    """Test the `search` command for splits."""
    console_output = StringIO()
    real_console = Console(file=console_output)

    mock_context_instance = mock_context.return_value
    mock_context_instance.console = real_console
    mock_context_instance.config = {"id": "test_corpus_id"}

    # Mock APIs
    mock_context_instance.split_api.vector_search.return_value = [
        MagicMock(file_id="file123", order=1, content="This is the first split..."),
        MagicMock(file_id="file456", order=2, content="This is the second split..."),
    ]
    mock_context_instance.file_api.get_file.side_effect = [
        MagicMock(path="/path/to/file1"),
        MagicMock(path="/path/to/file2"),
    ]

    # Run the command
    result = runner.invoke(
        app,
        ["search", "example search", "--limit", "2"],
        obj=mock_context_instance,
    )
    output = console_output.getvalue()

    # Debugging Output
    print(f"CLI Output:\n{output}")
    print(f"Result Exit Code: {result.exit_code}")
    print(f"Result Output: {result.stdout}")

    # Assertions
    assert result.exit_code == 0
    assert "Searching for splits..." in output
    assert "File: /path/to/file1" in output
    assert "1 This is the first split..." in output
    assert "File: /path/to/file2" in output
    assert "2 This is the second split..." in output


@patch("corpora_cli.commands.split.ContextObject")
def test_list_command(mock_context):
    """Test the `list` command for listing splits by file path."""
    console_output = StringIO()
    real_console = Console(file=console_output)

    mock_context_instance = mock_context.return_value
    mock_context_instance.console = real_console
    mock_context_instance.config = {"id": "test_corpus_id"}

    # Mock APIs
    mock_context_instance.file_api.get_file_by_path.return_value = MagicMock(
        id="file123"
    )
    mock_context_instance.split_api.list_splits_for_file.return_value = [
        MagicMock(order=1, content="This is split one."),
        MagicMock(order=2, content="This is split two."),
    ]

    # Run the command
    result = runner.invoke(
        app,
        ["list", "some/path/to/file.txt"],
        obj=mock_context_instance,
    )
    output = console_output.getvalue()

    # Debugging Output
    print(f"CLI Output:\n{output}")
    print(f"Result Exit Code: {result.exit_code}")
    print(f"Result Output: {result.stdout}")

    # Assertions
    assert result.exit_code == 0
    assert "Asking for splits... some/path/to/file.txt" in output
    assert "1 This is split one." in output
    assert "2 This is split two." in output


@patch("corpora_cli.commands.split.ContextObject")
def test_search_invalid_limit(mock_context):
    """Test the `search` command with an invalid limit."""
    console_output = StringIO()
    real_console = Console(file=console_output)

    mock_context_instance = mock_context.return_value
    mock_context_instance.console = real_console

    # Run the command with invalid limit
    result = runner.invoke(
        app,
        ["search", "example search", "--limit", "0"],
        obj=mock_context_instance,
    )
    output = console_output.getvalue()

    # Debugging Output
    print(f"CLI Output:\n{output}")
    print(f"Result Exit Code: {result.exit_code}")
    print(f"Result Output: {result.stdout}")

    # Assertions
    assert result.exit_code != 0
    assert "Limit must be greater than 0" in result.stdout


@patch("corpora_cli.commands.split.ContextObject")
def test_search_missing_text(mock_context):
    """Test the `search` command with missing text."""
    console_output = StringIO()
    real_console = Console(file=console_output)

    mock_context_instance = mock_context.return_value
    mock_context_instance.console = real_console

    # Run the command without text argument
    result = runner.invoke(app, ["search"], obj=mock_context_instance)
    output = console_output.getvalue()

    # Debugging Output
    print(f"CLI Output:\n{output}")
    print(f"Result Exit Code: {result.exit_code}")
    print(f"Result Output: {result.stdout}")

    # Assertions
    assert result.exit_code != 0
    assert "Missing argument 'TEXT'" in result.stdout
