from io import StringIO
from unittest.mock import patch
from typer.testing import CliRunner
from rich.console import Console

from corpora_cli.commands.file import app

runner = CliRunner()


@patch("corpora_cli.commands.file.ContextObject")
def test_add_command(mock_context):
    """Test the `add` command for adding a file to a corpus."""
    console_output = StringIO()
    real_console = Console(file=console_output)

    mock_context_instance = mock_context.return_value
    mock_context_instance.console = real_console

    corpus_id = "test_corpus"
    path = "test_file.txt"

    result = runner.invoke(app, ["add", corpus_id, path], obj=mock_context_instance)
    output = console_output.getvalue()

    assert result.exit_code == 0
    assert f"Adding file at {path} to corpus {corpus_id}" in output


@patch("corpora_cli.commands.file.ContextObject")
def test_remove_command(mock_context):
    """Test the `remove` command for removing a file from a corpus."""
    console_output = StringIO()
    real_console = Console(file=console_output)

    mock_context_instance = mock_context.return_value
    mock_context_instance.console = real_console

    corpus_id = "test_corpus"
    file_id = "test_file_id"

    result = runner.invoke(
        app, ["remove", corpus_id, file_id], obj=mock_context_instance
    )
    output = console_output.getvalue()

    assert result.exit_code == 0
    assert f"Removing file {file_id} from corpus {corpus_id}" in output
