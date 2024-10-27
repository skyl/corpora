from datetime import timedelta
import pytest
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
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
    user, _ = User.objects.get_or_create(username="testuser")
    application, _ = Application.objects.get_or_create(
        name="Test App",
        client_id="testclientid",
        client_secret="testclientsecret",
        client_type=Application.CLIENT_CONFIDENTIAL,
        authorization_grant_type=Application.GRANT_CLIENT_CREDENTIALS,
    )
    access_token = AccessToken.objects.create(
        user=user,
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
        payload = {"name": "Test Corpus", "url": "https://example.com/repo"}
        response = await client.post("/corpus", json=payload, headers=headers)

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Test Corpus"
        assert data["url"] == "https://example.com/repo"

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
