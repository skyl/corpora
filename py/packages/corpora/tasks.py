import io
import tarfile
import hashlib
from celery import shared_task
from .models import Corpus, File as CorpusFile


def compute_checksum(content: bytes) -> str:
    """Compute checksum compatible with Git blob format."""
    size = str(len(content))
    sha = hashlib.sha1(f"blob {size}\0".encode() + content).hexdigest()
    return sha


@shared_task
def process_tarball(corpus_id: str, tarball: bytes) -> None:
    """
    Process a tarball by extracting each file and creating a `CorpusFile`
    entry for each extracted file in the database.
    """
    print(f"Processing tarball... {corpus_id}")
    corpus = Corpus.objects.get(id=corpus_id)

    with tarfile.open(fileobj=io.BytesIO(tarball), mode="r:gz") as tar:
        for member in tar.getmembers():
            if member.isfile():
                file_content = tar.extractfile(member).read()
                checksum = compute_checksum(file_content)
                print(f"{member.name}")
                print(f"{checksum}")

                # Save each extracted file as a `CorpusFile` entry
                cf = CorpusFile.objects.create(
                    corpus=corpus,
                    path=member.name,
                    content=file_content.decode("utf-8", errors="replace"),
                    checksum=checksum,
                )
                print(f"Created file: {cf}")


@shared_task
def simple_task():
    return "Simple task completed!"
