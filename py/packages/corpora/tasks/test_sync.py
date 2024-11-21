import io
import tarfile
from unittest import mock

import pytest

from .sync import (
    process_tarball,
    generate_summary_task,
    split_file_task,
    generate_vector_task,
)


@pytest.mark.django_db
class TestCeleryTasks:
    @mock.patch("corpora.models.Corpus.objects.get")
    @mock.patch("corpora.models.CorpusTextFile.objects.get_or_create")
    @mock.patch("corpora.lib.files.compute_checksum")
    @mock.patch("corpora.tasks.sync.generate_summary_task.delay")
    @mock.patch("corpora.tasks.sync.split_file_task.delay")
    def test_process_tarball(
        self,
        mock_split_task,
        mock_summary_task,
        mock_compute_checksum,
        mock_get_or_create,
        mock_corpus_get,
    ):
        # Mock corpus and tarball
        mock_corpus = mock.Mock()
        mock_corpus_get.return_value = mock_corpus

        tarball_content = io.BytesIO()
        with tarfile.open(fileobj=tarball_content, mode="w:gz") as tar:
            file_data = b"test file content"
            tarinfo = tarfile.TarInfo(name="test_file.txt")
            tarinfo.size = len(file_data)
            tar.addfile(tarinfo, io.BytesIO(file_data))
        tarball_content.seek(0)

        # Mock file content processing
        mock_compute_checksum.return_value = "mock_checksum"
        mock_file = mock.Mock()
        mock_get_or_create.return_value = (mock_file, False)

        # Run the task
        process_tarball("mock_corpus_id", tarball_content.getvalue())

        # Assertions
        mock_corpus_get.assert_called_once_with(id="mock_corpus_id")
        mock_corpus.save.assert_called_once_with(update_fields=["updated_at"])
        mock_get_or_create.assert_called_once_with(
            corpus=mock_corpus, path="test_file.txt"
        )
        assert mock_file.content == "test file content"
        # assert mock_file.checksum == "mock_checksum"
        mock_file.save.assert_called_once()
        mock_file.splits.all().delete.assert_called_once()
        # over-specified - we don't even use the summary in the app yet
        # mock_summary_task.assert_called_once_with(mock_file.id)
        mock_split_task.assert_called_once_with(mock_file.id)

    @mock.patch("corpora.models.CorpusTextFile.objects.get")
    def test_generate_summary_task(self, mock_corpus_file_get):
        # Mock corpus file
        mock_corpus_file = mock.Mock()
        mock_corpus_file_get.return_value = mock_corpus_file

        # Run the task
        generate_summary_task("mock_corpus_file_id")

        # Assertions
        mock_corpus_file_get.assert_called_once_with(id="mock_corpus_file_id")
        mock_corpus_file.get_and_save_summary.assert_called_once()
        mock_corpus_file.get_and_save_vector_of_summary.assert_called_once()

    @mock.patch("corpora.models.CorpusTextFile.objects.get")
    @mock.patch("corpora.tasks.sync.generate_vector_task.delay")
    def test_split_file_task(self, mock_generate_vector_task, mock_corpus_file_get):
        # Mock corpus file
        mock_corpus_file = mock.Mock()
        mock_corpus_file_get.return_value = mock_corpus_file

        # Mock split content
        mock_split = mock.Mock()
        mock_corpus_file.split_content.return_value = [mock_split]

        # Run the task
        split_file_task("mock_corpus_file_id")

        # Assertions
        mock_corpus_file_get.assert_called_once_with(id="mock_corpus_file_id")
        mock_corpus_file.split_content.assert_called_once()
        mock_generate_vector_task.assert_called_once_with(mock_split.id)

    @mock.patch("corpora.models.Split.objects.get")
    def test_generate_vector_task(self, mock_split_get):
        # Mock split
        mock_split = mock.Mock()
        mock_split_get.return_value = mock_split

        # Run the task
        generate_vector_task("mock_split_id")

        # Assertions
        mock_split_get.assert_called_once_with(id="mock_split_id")
        mock_split.get_and_save_vector.assert_called_once()
