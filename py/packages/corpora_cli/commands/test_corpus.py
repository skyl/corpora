from unittest.mock import patch, Mock
from io import StringIO
from typer.testing import CliRunner
from rich.console import Console

from corpora_client.exceptions import ApiException
from corpora_cli.commands.corpus import app


runner = CliRunner()


@patch("corpora_cli.commands.corpus.save_config")
@patch("corpora_cli.commands.corpus.Path")
@patch("corpora_cli.commands.corpus.get_best_collector")
@patch("corpora_cli.commands.corpus.ContextObject")
def test_init_command(
    mock_context, mock_get_best_collector, mock_path, mock_save_config
):
    """Test the `init` command for basic behavior."""
    # Create a real console and capture output in a StringIO buffer
    console_output = StringIO()
    real_console = Console(file=console_output)

    # Setup mock context with a real console and config
    mock_context_instance = mock_context.return_value
    mock_context_instance.console = real_console
    mock_context_instance.config = {
        "name": "test_repo",
        "url": "https://github.com/test/repo",
    }

    # Mock Path.exists to simulate missing config file
    mock_path.return_value.exists.return_value = False

    # Mock collector behavior
    mock_collector = mock_get_best_collector.return_value
    mock_collector.collect_files.return_value = ["file1", "file2"]
    mock_collector.create_tarball.return_value.getvalue.return_value = (
        b"tarball_content"
    )

    # Mock API response
    mock_create_corpus_response = Mock()
    mock_create_corpus_response.id = "12345"
    mock_create_corpus_response.name = "test_repo"
    mock_context_instance.corpus_api.create_corpus.return_value = (
        mock_create_corpus_response
    )

    # Run the command
    result = runner.invoke(app, ["init"], obj=mock_context_instance)

    # Capture console output
    output = console_output.getvalue()

    # Verify output and behavior
    assert result.exit_code == 0
    assert "Initializing a new corpus..." in output
    assert "Gathering files..." in output
    assert "Collected 2 files." in output
    assert "Uploading corpus tarball to server..." in output
    assert "test_repo created!" in output
    assert "Corpus ID saved to .corpora/.id" in output

    # Verify create_corpus was called with correct parameters
    mock_context_instance.corpus_api.create_corpus.assert_called_once_with(
        name="test_repo",
        url="https://github.com/test/repo",
        tarball=b"tarball_content",
    )

    # Verify config file was saved twice with the correct data
    assert mock_save_config.call_count == 1
    mock_save_config.assert_any_call(
        {
            "name": "test_repo",
            "url": "https://github.com/test/repo",
        }
    )


@patch("corpora_cli.commands.corpus.ContextObject")
def test_delete_command(mock_context):
    """Test the `delete` command for basic deletion."""
    console_output = StringIO()
    real_console = Console(file=console_output)

    mock_context_instance = mock_context.return_value
    mock_context_instance.console = real_console
    # Set `config["name"]` to return "test_corpus" instead of a MagicMock object
    mock_context_instance.config = {"name": "test_corpus"}

    result = runner.invoke(app, ["delete"], obj=mock_context_instance)
    output = console_output.getvalue()

    assert result.exit_code == 0
    assert "Deleting corpus: test_corpus" in output
    assert "test_corpus deleted" in output
    mock_context_instance.corpus_api.delete_corpus.assert_called_once_with(
        "test_corpus"
    )


@patch("corpora_cli.commands.corpus.ContextObject")
def test_delete_command_corpus_not_found(mock_context):
    """Test the `delete` command for a non-existent corpus."""
    console_output = StringIO()
    real_console = Console(file=console_output)

    mock_context_instance = mock_context.return_value
    mock_context_instance.console = real_console
    mock_context_instance.config = {"name": "test_corpus"}

    # Use ApiException with a status attribute to simulate 404 response
    mock_context_instance.corpus_api.delete_corpus.side_effect = ApiException(
        status=404
    )

    result = runner.invoke(app, ["delete"], obj=mock_context_instance)
    output = console_output.getvalue()

    assert result.exit_code == 1
    assert "Corpus not found." in output


# Test for `list` command
@patch("corpora_cli.commands.corpus.ContextObject")
def test_list_command(mock_context):
    """Test the `list` command for listing corpora."""
    console_output = StringIO()
    real_console = Console(file=console_output)

    mock_context_instance = mock_context.return_value
    mock_context_instance.console = real_console
    mock_context_instance.corpus_api.list_corpora.return_value = [
        Mock(name="Corpus 1"),
        Mock(name="Corpus 2"),
    ]

    result = runner.invoke(app, ["list"], obj=mock_context_instance)
    output = console_output.getvalue()

    assert result.exit_code == 0
    assert "Corpus 1" in output
    assert "Corpus 2" in output


@patch("corpora_cli.commands.corpus.ContextObject")
def test_print_command(mock_context):
    """Test the `print` command for rich output examples."""
    console_output = StringIO()
    real_console = Console(file=console_output)

    mock_context_instance = mock_context.return_value
    mock_context_instance.console = real_console

    result = runner.invoke(app, ["print"], obj=mock_context_instance)
    output = console_output.getvalue()

    assert result.exit_code == 0
    # Minimal assertions for predictable output
    assert "Hello World" in output
    assert "Sample Table" in output
    assert "This is a log message." in output
    assert "Panel Title" in output
    assert "This is inside a panel." in output
