from unittest.mock import patch
from datetime import timedelta
import pytest
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile
from ninja.testing import TestAsyncClient
from oauth2_provider.models import AccessToken, Application
from asgiref.sync import sync_to_async

from .corpus import corpus_router
from .test_lib import create_user_and_token, create_corpus

User = get_user_model()
client = TestAsyncClient(corpus_router)


class CorpusAPITestCase(TestCase):
    @pytest.mark.django_db
    async def test_create_corpus(self):
        """Test creating a corpus with an uploaded tarball."""
        _, headers = await create_user_and_token()
        data = {"name": "Test Corpus", "url": "https://example.com/repo"}
        file_content = b"Dummy tarball content"
        file = SimpleUploadedFile(
            "test.tar.gz", file_content, content_type="application/gzip"
        )

        with patch("corpora.tasks.process_tarball.delay") as mock_delay:
            response = await client.post(
                "", data=data, FILES={"tarball": file}, headers=headers
            )
            response_data = response.json()
            mock_delay.assert_called_once_with(response_data["id"], file_content)
            assert response.status_code == 201
            assert response_data["name"] == "Test Corpus"
            assert response_data["url"] == "https://example.com/repo"

    @pytest.mark.django_db
    async def test_create_corpus_conflict(self):
        """Test creating a corpus with a duplicate name for the same user."""
        user, headers = await create_user_and_token()
        await create_corpus("Duplicate Corpus", "https://example.com", user)
        data = {"name": "Duplicate Corpus", "url": "https://example.com/repo"}
        file_content = b"Dummy tarball content"
        file = SimpleUploadedFile(
            "test.tar.gz", file_content, content_type="application/gzip"
        )

        response = await client.post(
            "", data=data, FILES={"tarball": file}, headers=headers
        )
        assert response.status_code == 409
        assert (
            response.json()["detail"]
            == "A corpus with this name already exists for this owner."
        )

    @pytest.mark.django_db
    async def test_get_corpus(self):
        """Test retrieving a corpus by ID."""
        user, headers = await create_user_and_token()
        corpus = await create_corpus("Retrieve Corpus", "https://example.com", user)

        response = await client.get(f"/{corpus.id}", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Retrieve Corpus"
        assert data["url"] == "https://example.com"

    @pytest.mark.django_db
    async def test_get_corpus_not_found(self):
        """Test retrieving a non-existent corpus."""
        _, headers = await create_user_and_token()
        response = await client.get(
            "/00000000-0000-0000-0000-000000000000", headers=headers
        )
        assert response.status_code == 404

    @pytest.mark.django_db
    async def test_delete_corpus(self):
        """Test deleting a corpus by name."""
        user, headers = await create_user_and_token()
        corpus = await create_corpus("Deletable Corpus", "https://example.com", user)

        response = await client.delete(f"?corpus_name={corpus.name}", headers=headers)
        assert response.status_code == 204
        assert response.json() == "Corpus deleted."

    @pytest.mark.django_db
    async def test_delete_corpus_not_found(self):
        """Test deleting a non-existent corpus."""
        _, headers = await create_user_and_token()
        response = await client.delete(
            "?corpus_name=NonExistentCorpus", headers=headers
        )
        assert response.status_code == 404

    @pytest.mark.django_db
    async def test_list_corpora(self):
        """Test listing all corpora for the authenticated user."""
        user, headers = await create_user_and_token()
        await create_corpus("Corpus 1", "https://example.com/1", user)
        await create_corpus("Corpus 2", "https://example.com/2", user)

        other_user = await sync_to_async(User.objects.create_user)(username="otheruser")
        await create_corpus("Other User Corpus", "https://other.com", other_user)

        response = await client.get("", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["name"] == "Corpus 1"
        assert data[1]["name"] == "Corpus 2"
