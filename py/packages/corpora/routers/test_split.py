import pytest
from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth import get_user_model
from ninja.testing import TestAsyncClient

from .split import split_router
from .test_lib import (
    create_user_and_token,
    create_corpus,
    create_file,
    create_split,
)


User = get_user_model()
client = TestAsyncClient(split_router)


class SplitAPITestCase(TestCase):
    @pytest.mark.django_db
    async def test_get_split(self):
        """Test retrieving a split by ID."""
        user, headers = await create_user_and_token()
        corpus = await create_corpus(
            "Test Corpus", "https://example.com/repo", user
        )
        file = await create_file(corpus, "file1.txt", "Sample content")
        split = await create_split(file, "Split content", [0.1] * 1536)

        response = await client.get(f"/{split.id}", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["content"] == "Split content"
        assert data["file_id"] == str(file.id)

    @pytest.mark.django_db
    async def test_list_splits_for_file(self):
        """Test listing all splits for a specific file."""
        user, headers = await create_user_and_token()
        corpus = await create_corpus(
            "Test Corpus", "https://example.com/repo", user
        )
        file = await create_file(corpus, "file1.txt", "Sample content")
        await create_split(file, "Split content 1", [0.1] * 1536, order=1)
        await create_split(file, "Split content 2", [0.2] * 1536, order=2)

        response = await client.get(f"/file/{file.id}", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["content"] == "Split content 1"
        assert data[1]["content"] == "Split content 2"

    @pytest.mark.django_db
    async def test_vector_search_splits(self):
        """Test performing a vector similarity search on splits."""
        user, headers = await create_user_and_token()
        corpus = await create_corpus(
            "Test Corpus", "https://example.com/repo", user
        )
        file = await create_file(corpus, "file1.txt", "Sample content")
        await create_split(file, "Split content 1", [0.1] * 1536, order=1)
        await create_split(file, "Split content 2", [0.2] * 1536, order=2)

        payload = {
            "text": "foobar",
            "corpus_id": str(corpus.id),
            "limit": 2,
        }

        # Mock the load_llm_provider and its get_embedding function
        with patch(
            "corpora_ai.provider_loader.load_llm_provider"
        ) as mock_llm_provider:
            mock_llm_instance = mock_llm_provider.return_value
            mock_llm_instance.get_embedding.return_value = [
                0.1
            ] * 1536  # Mocked embedding

            # Execute the test request
            response = await client.post(
                "/search", json=payload, headers=headers
            )
            print(response.content)

            # Assertions
            assert response.status_code == 200
            data = response.json()
            assert len(data) > 0  # Should return at least one similar split
            mock_llm_instance.get_embedding.assert_called_once_with("foobar")
