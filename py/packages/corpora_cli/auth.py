import requests
import typer


def authenticate(client_id: str, client_secret: str) -> str:
    """Authenticate using OAuth2 Client Credentials and return an access token."""
    response = requests.post(
        "http://localhost:8000/o/token/",
        data={
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
        },
    )

    if response.status_code != 200:
        typer.echo("Authentication failed", err=True)
        raise typer.Exit(code=1)

    return response.json()["access_token"]
