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

from .api import api
from .models import Corpus, File

User = get_user_model()
client = TestAsyncClient(api)


# Helper functions to generate an access token and headers
@sync_to_async
def create_user_and_token():
    user, _ = User.objects.get_or_create(
        username="testuser", defaults={"password": "password123"}
    )
    application, _ = Application.objects.get_or_create(
        name="Test App",
        client_id="testclientid",
        client_secret="testclientsecret",
        client_type=Application.CLIENT_CONFIDENTIAL,
        authorization_grant_type=Application.GRANT_CLIENT_CREDENTIALS,
        user=user,
    )
    access_token = AccessToken.objects.create(
        # user=user,
        application=application,
        token="testaccesstoken",
        expires=timezone.now() + timedelta(days=1),
    )
    return user, {"Authorization": f"Bearer {access_token.token}"}


@sync_to_async
def create_corpus(name, url, owner):
    return Corpus.objects.create(name=name, url=url, owner=owner)


@sync_to_async
def create_file(corpus, path, content):
    return File.objects.create(corpus=corpus, path=path, content=content)


class APITestCase(TestCase):
    @pytest.mark.django_db
    async def test_create_corpus(self):
        _, headers = await create_user_and_token()

        # Form data
        data = {
            "name": "Test Corpus",
            "url": "https://example.com/repo",
        }

        # Create a sample tar.gz file
        file_content = b"Dummy tarball content"
        file = SimpleUploadedFile(
            "test.tar.gz", file_content, content_type="application/gzip"
        )

        # Mock process_tarball.delay to prevent it from connecting to Redis
        with patch("corpora.tasks.process_tarball.delay") as mock_delay:
            response = await client.post(
                "/corpus",
                data=data,
                FILES={"tarball": file},
                headers=headers,
            )

            # Ensure the Celery task is called with the expected arguments
            mock_delay.assert_called_once_with(file_content)

            # Check the response and returned data
            assert response.status_code == 201
            response_data = response.json()
            assert response_data["name"] == "Test Corpus"
            assert response_data["url"] == "https://example.com/repo"

    @pytest.mark.django_db
    async def test_get_corpus(self):
        user, headers = await create_user_and_token()
        corpus = await create_corpus("Retrieve Corpus", "https://example.com", user)

        response = await client.get(f"/corpus/{corpus.id}", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Retrieve Corpus"

    @pytest.mark.django_db
    async def test_get_corpus_not_found(self):
        _, headers = await create_user_and_token()
        response = await client.get(
            "/corpus/00000000-0000-0000-0000-000000000000", headers=headers
        )
        assert response.status_code == 404

    @pytest.mark.django_db
    async def test_create_file(self):
        user, headers = await create_user_and_token()
        corpus = await create_corpus("File Corpus", "https://example.com/repo", user)
        payload = {
            "path": "file1.txt",
            "content": "Sample content",
            "corpus_id": str(corpus.id),
        }

        response = await client.post("/file", json=payload, headers=headers)
        assert response.status_code == 201
        data = response.json()
        assert data["path"] == "file1.txt"

    @pytest.mark.django_db
    async def test_get_file(self):
        user, headers = await create_user_and_token()
        corpus = await create_corpus(
            "Retrieve File Corpus", "https://example.com/repo", user
        )
        file = await create_file(corpus, "file1.txt", "Sample content")

        response = await client.get(f"/file/{file.id}", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["path"] == "file1.txt"

    @pytest.mark.django_db
    async def test_get_file_not_found(self):
        _, headers = await create_user_and_token()
        response = await client.get(
            "/file/00000000-0000-0000-0000-000000000000", headers=headers
        )
        assert response.status_code == 404

    @pytest.mark.django_db
    async def test_list_corpora(self):
        # Set up the user and headers
        user, headers = await create_user_and_token()

        # Create corpora for this user
        await create_corpus("Corpus 1", "https://example.com/1", user)
        await create_corpus("Corpus 2", "https://example.com/2", user)

        # Create a corpus for another user to verify filtering
        other_user = await sync_to_async(User.objects.create_user)(username="otheruser")
        await create_corpus("Other User Corpus", "https://other.com", other_user)

        # Make the request
        response = await client.get("/corpus", headers=headers)

        # Verify the response
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["name"] == "Corpus 1"
        assert data[1]["name"] == "Corpus 2"
