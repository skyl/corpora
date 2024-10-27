import pytest
from django.test import TestCase
from ninja.testing import TestAsyncClient
from .api import api  # Ensure this imports your actual NinjaAPI instance
from .models import Corpus, File


# Instantiate TestClient for the NinjaAPI
client = TestAsyncClient(api)


class APITestCase(TestCase):
    @pytest.mark.django_db
    async def test_create_corpus(self):
        payload = {"name": "Test Corpus", "url": "https://example.com/repo"}
        response = await client.post("/corpus", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Test Corpus"
        assert data["url"] == "https://example.com/repo"

    @pytest.mark.django_db
    async def test_get_corpus(self):
        # Create a corpus directly in the DB to retrieve it
        corpus = await Corpus.objects.acreate(
            name="Retrieve Corpus", url="https://example.com"
        )
        response = await client.get(f"/corpus/{corpus.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Retrieve Corpus"

    @pytest.mark.django_db
    async def test_get_corpus_not_found(self):
        response = await client.get("/corpus/00000000-0000-0000-0000-000000000000")
        assert response.status_code == 404

    @pytest.mark.django_db
    async def test_create_file(self):
        corpus = await Corpus.objects.acreate(
            name="File Corpus", url="https://example.com/repo"
        )
        payload = {
            "path": "file1.txt",
            "content": "Sample content",
            "corpus_id": str(corpus.id),
        }
        response = await client.post("/file", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["path"] == "file1.txt"

    @pytest.mark.django_db
    async def test_get_file(self):
        corpus = await Corpus.objects.acreate(
            name="Retrieve File Corpus", url="https://example.com/repo"
        )
        file = await File.objects.acreate(
            path="file1.txt", content="Sample content", corpus=corpus
        )
        response = await client.get(f"/file/{file.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["path"] == "file1.txt"

    @pytest.mark.django_db
    async def test_get_file_not_found(self):
        response = await client.get("/file/00000000-0000-0000-0000-000000000000")
        assert response.status_code == 404
