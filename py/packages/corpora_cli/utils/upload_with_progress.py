import io

# TODO: use api_client instead of requests
import requests
from rich.progress import track

from corpora_client.api.corpora_api import CorporaApi


def upload_with_progress(
    api_client: CorporaApi, tarball: io.BytesIO, filename: str, url: str
):
    """Upload the tarball to the server with a progress bar using rich."""
    tarball.seek(0)
    file_size = len(tarball.getvalue())
    chunk_size = 1024 * 1024  # 1 MB chunks

    # Wrap tarball in a generator for streaming
    def file_chunk_generator(file_obj):
        for chunk in iter(lambda: file_obj.read(chunk_size), b""):
            yield chunk

    # Calculate total number of chunks
    total_chunks = (file_size + chunk_size - 1) // chunk_size

    # Upload file in chunks with progress tracking
    response = requests.post(
        url,
        files={"file": (filename, file_chunk_generator(tarball), "application/gzip")},
        headers={"Authorization": f"Bearer {api_client.access_token}"},
        stream=True,
    )

    for _ in track(range(total_chunks), description="Uploading..."):
        next(file_chunk_generator(tarball))

    response.raise_for_status()
    return response.json()
