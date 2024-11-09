from io import StringIO
from unittest.mock import patch, MagicMock
from typer.testing import CliRunner
from rich.console import Console

# from corpora_client.models.split_vector_search_schema import SplitVectorSearchSchema
from corpora_client.api.split_api import SplitApi
from corpora_cli.context import ContextObject
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
        # this frustratingly doesn't work
        # ["search", "example search", "2"],
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


# @patch("corpora_cli.commands.split.ContextObject")
# def test_search_no_results(mock_context_class):
#     """Test the search command with no results."""
#     console_output = StringIO()
#     real_console = Console(file=console_output)

#     mock_context_instance = mock_context_class.return_value
#     mock_context_instance.console = real_console
#     mock_context_instance.config = {"id": "test_corpus_id"}
#     mock_context_instance.split_api = MagicMock(spec=SplitApi)

#     # Mock split_api response with no results
#     mock_context_instance.split_api.vector_search.return_value = []

#     result = runner.invoke(app, ["search 'example search'"], obj=mock_context_instance)
#     output = console_output.getvalue()

#     assert result.exit_code == 0
#     assert "Searching for splits..." in output
#     assert "No splits found." in output


@patch("corpora_cli.commands.split.ContextObject")
def test_search_invalid_input(mock_context_class):
    """Test the search command with invalid inputs."""
    console_output = StringIO()
    real_console = Console(file=console_output)

    mock_context_instance = mock_context_class.return_value
    mock_context_instance.console = real_console

    # # Missing text argument
    # result = runner.invoke(app, ["search"], obj=mock_context_instance)
    # output = console_output.getvalue()
    # assert result.exit_code != 0
    # print(f"CLI Output:\n{output}")
    # print(f"Result Exit Code: {result.exit_code}")
    # print(f"Result Output: {result.stdout}")

    # assert "Missing argument 'TEXT'" in result.stdout

    # Invalid limit
    result = runner.invoke(
        app,
        ["search", '"example search"', "--limit", "0"],
        obj=mock_context_instance,
    )
    output = console_output.getvalue()
    assert result.exit_code != 0
    print(f"CLI Output:\n{output}")
    print(f"Result Exit Code: {result.exit_code}")
    print(f"Result Output: {result.stdout}")
    assert "Limit must be greater than 0" in result.stdout
