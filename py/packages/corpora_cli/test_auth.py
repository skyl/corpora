import os
import pytest
from unittest.mock import patch, MagicMock
from corpora_cli.auth import AuthResolver, AuthError


@pytest.fixture
def config():
    return {"auth": {"token_url": "http://testserver/o/token/"}}


@pytest.fixture
def auth_resolver(config):
    return AuthResolver(config)


def test_resolve_auth_success_with_env_credential(auth_resolver):
    # Mock environment variable CREDENTIAL
    with patch.dict(os.environ, {"CREDENTIAL": "encodedcredential"}):
        with patch.object(
            auth_resolver, "_request_token_with_basic_auth", return_value="test_token"
        ) as mock_request:
            token = auth_resolver.resolve_auth()
            assert token == "test_token"
            mock_request.assert_called_once_with("encodedcredential")


def test_resolve_auth_success_with_client_credentials(auth_resolver):
    # Mock client ID and secret in environment variables
    with patch.dict(
        os.environ,
        {"CORPORA_CLIENT_ID": "test_id", "CORPORA_CLIENT_SECRET": "test_secret"},
    ):
        with patch.object(
            auth_resolver, "_request_token_with_basic_auth", return_value="test_token"
        ) as mock_request:
            token = auth_resolver.resolve_auth()
            encoded_credentials = auth_resolver._encode_credentials(
                "test_id", "test_secret"
            )
            assert token == "test_token"
            mock_request.assert_called_once_with(encoded_credentials)


def test_resolve_auth_missing_credentials(auth_resolver):
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(AuthError) as excinfo:
            auth_resolver.resolve_auth()
        assert "No valid authentication method available." in str(excinfo.value)


def test_request_token_with_basic_auth_success(auth_resolver):
    # Mock the response of the requests.post call
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"access_token": "test_access_token"}
    with patch("requests.post", return_value=mock_response) as mock_post:
        token = auth_resolver._request_token_with_basic_auth("encodedcredential")
        assert token == "test_access_token"
        mock_post.assert_called_once_with(
            auth_resolver.token_url,
            headers={
                "Authorization": "Basic encodedcredential",
                "Cache-Control": "no-cache",
                "Content-Type": "application/x-www-form-urlencoded",
            },
            data={"grant_type": "client_credentials"},
            timeout=10,
        )


def test_encode_credentials(auth_resolver):
    encoded = auth_resolver._encode_credentials("test_id", "test_secret")
    assert (
        encoded == "dGVzdF9pZDp0ZXN0X3NlY3JldA=="
    )  # This is base64 encoding of "test_id:test_secret"
