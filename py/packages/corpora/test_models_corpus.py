import pytest
from unittest.mock import patch, MagicMock
from django.contrib.auth import get_user_model
from corpora.models import (
    Corpus,
    Split,
    CorpusTextFile,
)

User = get_user_model()


@pytest.mark.django_db
class TestCorpusModelMethods:
    @pytest.fixture
    def user(self):
        return User.objects.create_user(username="testuser", password="testpassword")

    @pytest.fixture
    def corpus(self, user):
        return Corpus.objects.create(
            name="Test Corpus", owner=user, url="https://example.com"
        )

    @pytest.fixture
    def file(self, corpus):
        # Create a file associated with the corpus
        return CorpusTextFile.objects.create(
            corpus=corpus, path="test.txt", checksum="abc123", content="File content"
        )

    @pytest.fixture
    def mock_splits(self, file):
        # Create Split objects associated with the file
        split1 = Split.objects.create(
            file=file,
            content="Content 1",
            vector=[0.1] * 1536,
            order=1,
        )
        split2 = Split.objects.create(
            file=file,
            content="Content 2",
            vector=[0.2] * 1536,
            order=2,
        )
        return [split1, split2]

    def test_get_relevant_splits(self, corpus, mock_splits):
        with patch(
            "corpora_ai.provider_loader.load_llm_provider"
        ) as mock_load_llm_provider:
            mock_llm = MagicMock()
            mock_load_llm_provider.return_value = mock_llm
            mock_llm.get_embedding.return_value = [0.1] * 1536

            splits = corpus.get_relevant_splits("Test query", limit=5)

            assert len(splits) == 2
            assert splits[0].content == "Content 1"
            assert splits[1].content == "Content 2"
            mock_llm.get_embedding.assert_called_once_with("Test query")

    def test_get_relevant_splits_context(self, corpus, mock_splits):
        with patch(
            "corpora_ai.provider_loader.load_llm_provider"
        ) as mock_load_llm_provider:
            mock_llm = MagicMock()
            mock_load_llm_provider.return_value = mock_llm
            mock_llm.get_embedding.return_value = [0.1] * 1536

            context = corpus.get_relevant_splits_context("Test query", limit=5)

            assert "Content 1" in context
            assert "Content 2" in context
            assert "```\n" in context
            mock_llm.get_embedding.assert_called_once_with("Test query")

    def test_get_file_hashes(self, corpus, file):
        # Test that the file hashes are retrieved correctly
        file_hashes = corpus.get_file_hashes()

        assert len(file_hashes) == 1
        assert file_hashes["test.txt"] == "abc123"

    def test_delete_files(self, corpus, file):
        # Test deleting files by path
        corpus.delete_files(["test.txt"])

        remaining_files = corpus.files.all()

        assert remaining_files.count() == 0
