import pytest
from django.test import TestCase
from django.contrib.auth import get_user_model
from ninja.testing import TestAsyncClient

from .corpustextfile import file_router
from .test_lib import create_user_and_token, create_corpus, create_file

User = get_user_model()
client = TestAsyncClient(file_router)


class CorpusTextFileAPITestCase(TestCase):
    @pytest.mark.django_db
    async def test_get_file_by_path(self):
        """Test retrieving a file by path within a corpus."""
        user, headers = await create_user_and_token()
        corpus = await create_corpus(
            "Path Retrieval Corpus", "https://example.com/repo", user
        )
        await create_file(corpus, "nested/file1.txt", "Sample content")

        response = await client.get(
            f"/corpus/{corpus.id}?path=nested/file1.txt", headers=headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["path"] == "nested/file1.txt"
        assert data["content"] == "Sample content"
        assert data["corpus_id"] == str(corpus.id)

    @pytest.mark.django_db
    async def test_get_file_by_path_not_found(self):
        """Test retrieving a non-existent file by path."""
        user, headers = await create_user_and_token()
        corpus = await create_corpus(
            "Nonexistent File Corpus", "https://example.com/repo", user
        )

        response = await client.get(
            f"/corpus/{corpus.id}?path=nonexistent/file.txt", headers=headers
        )
        assert response.status_code == 404

    @pytest.mark.django_db
    async def test_get_file_by_path_missing_query_param(self):
        """Test retrieving a file by path without providing the required query parameter."""
        user, headers = await create_user_and_token()
        corpus = await create_corpus(
            "Missing Query Param Corpus", "https://example.com/repo", user
        )

        response = await client.get(f"/corpus/{corpus.id}", headers=headers)
        assert response.status_code == 422
        assert response.json()["detail"][0]["msg"] == "Field required"
        assert response.json()["detail"][0]["loc"] == ["query", "path"]

    @pytest.mark.django_db
    async def test_create_file(self):
        """Test creating a file within a corpus."""
        user, headers = await create_user_and_token()
        corpus = await create_corpus("File Corpus", "https://example.com/repo", user)
        payload = {
            "path": "file1.txt",
            "content": "Sample content",
            "corpus_id": str(corpus.id),
        }

        response = await client.post("", json=payload, headers=headers)
        assert response.status_code == 201
        data = response.json()
        assert data["path"] == "file1.txt"
        assert data["content"] == "Sample content"
        assert data["corpus_id"] == str(corpus.id)

    @pytest.mark.django_db
    async def test_create_file_with_duplicate_path(self):
        """Test creating a file with a duplicate path within the same corpus."""
        user, headers = await create_user_and_token()
        corpus = await create_corpus("File Corpus", "https://example.com/repo", user)
        await create_file(corpus, "file1.txt", "Sample content")

        payload = {
            "path": "file1.txt",
            "content": "New content",
            "corpus_id": str(corpus.id),
        }

        response = await client.post("", json=payload, headers=headers)
        assert response.status_code == 409
        assert (
            response.json()["detail"]
            == "A file with this path already exists in the corpus."
        )

    @pytest.mark.django_db
    async def test_get_file(self):
        """Test retrieving a file by ID."""
        user, headers = await create_user_and_token()
        corpus = await create_corpus(
            "Retrieve File Corpus", "https://example.com/repo", user
        )
        file = await create_file(corpus, "file1.txt", "Sample content")

        response = await client.get(f"/{file.id}", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["path"] == "file1.txt"
        assert data["content"] == "Sample content"
        assert data["corpus_id"] == str(corpus.id)

    @pytest.mark.django_db
    async def test_get_file_not_found(self):
        """Test retrieving a non-existent file."""
        _, headers = await create_user_and_token()
        response = await client.get(
            "/00000000-0000-0000-0000-000000000000", headers=headers
        )
        assert response.status_code == 404
