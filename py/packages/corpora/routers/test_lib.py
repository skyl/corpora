from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone
from asgiref.sync import sync_to_async
from oauth2_provider.models import AccessToken, Application

from corpora.models import Corpus, CorpusTextFile, Split

User = get_user_model()


# Helper function to generate user and token
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
        token="testaccesstoken",
        application=application,
        expires=timezone.now() + timedelta(days=1),
    )
    return user, {"Authorization": f"Bearer {access_token.token}"}


# Helper function to create a Corpus instance
@sync_to_async
def create_corpus(name, url, owner):
    return Corpus.objects.create(name=name, url=url, owner=owner)


@sync_to_async
def create_file(corpus, path, content):
    return CorpusTextFile.objects.create(corpus=corpus, path=path, content=content)


@sync_to_async
def create_split(file, content, vector, order=0):
    return Split.objects.create(file=file, content=content, vector=vector, order=order)
