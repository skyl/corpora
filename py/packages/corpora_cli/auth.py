import os
import base64
import requests
import typer
from typing import Optional, Dict, Any


class AuthError(Exception):
    """Custom exception for authentication errors."""

    pass


class AuthResolver:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        base_url = config.get("base_url", "http://corpora_app:8877")
        self.token_url = f"{base_url}/o/token/"

    def resolve_auth(self) -> str:
        """
        Attempts to authenticate using available methods.
        Current supported methods: Client Credentials.

        Returns:
            str: Bearer token on successful authentication.

        Raises:
            AuthError: If no valid authentication method is available.
        """
        auth_token = self._authenticate_with_client_credentials()
        if auth_token:
            return auth_token

        raise AuthError("No valid authentication method available.")

    def _authenticate_with_client_credentials(self) -> Optional[str]:
        """
        Authenticate using client credentials from environment variables or config file.

        Returns:
            Optional[str]: Access token if authentication is successful, otherwise None.
        """
        # Attempt to get credentials from environment variables or config
        credential = os.getenv("CREDENTIAL")
        client_id = os.getenv("CORPORA_CLIENT_ID") or self.config.get("auth", {}).get(
            "client_id"
        )
        client_secret = os.getenv("CORPORA_CLIENT_SECRET") or self.config.get(
            "auth", {}
        ).get("client_secret")

        if credential:
            # Use pre-encoded credential if available
            typer.echo("Authenticating with encoded client credentials...")
            return self._request_token_with_basic_auth(credential)
        elif client_id and client_secret:
            # Encode client_id and client_secret in base64 for Basic Auth header
            typer.echo("Authenticating by encoding client credentials...")
            return self._request_token_with_basic_auth(
                self._encode_credentials(client_id, client_secret)
            )

        typer.echo(
            "Client credentials not found in environment or configuration.", err=True
        )
        return None

    def _encode_credentials(self, client_id: str, client_secret: str) -> str:
        """
        Encode client_id and client_secret to Base64 for Basic Authorization header.

        Args:
            client_id (str): OAuth client ID.
            client_secret (str): OAuth client secret.

        Returns:
            str: Base64 encoded credentials.
        """
        credential = f"{client_id}:{client_secret}"
        return base64.b64encode(credential.encode("utf-8")).decode("utf-8")

    def _request_token_with_basic_auth(self, credential: str) -> str:
        """
        Requests an access token using HTTP Basic Authentication.

        Args:
            credential (str): Base64 encoded client credentials.

        Returns:
            str: Access token.

        Raises:
            AuthError: If authentication fails.
        """
        headers = {
            "Authorization": f"Basic {credential}",
            "Cache-Control": "no-cache",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {"grant_type": "client_credentials"}

        response = requests.post(self.token_url, headers=headers, data=data, timeout=10)
        response.raise_for_status()
        return response.json().get("access_token")
