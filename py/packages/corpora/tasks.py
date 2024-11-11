import io
import tarfile

from celery import shared_task

from .lib.files import compute_checksum
from .models import Corpus, CorpusTextFile, Split


@shared_task
def process_tarball(corpus_id: str, tarball: bytes) -> None:
    corpus = Corpus.objects.get(id=corpus_id)
    corpus.save(update_fields=["updated_at"])
    with tarfile.open(fileobj=io.BytesIO(tarball), mode="r:gz") as tar:
        for member in tar.getmembers():
            if member.isfile():
                file_content = (
                    tar.extractfile(member).read().decode("utf-8", errors="replace")
                )
                checksum = compute_checksum(file_content)

                corpus_file, _ = CorpusTextFile.objects.get_or_create(
                    corpus=corpus,
                    path=member.name,
                )
                corpus_file.content = file_content
                corpus_file.checksum = checksum
                corpus_file.save()
                corpus_file.splits.all().delete()

                generate_summary_task.delay(corpus_file.id)
                split_file_task.delay(corpus_file.id)


@shared_task
def generate_summary_task(corpus_file_id: str) -> None:
    corpus_file = CorpusTextFile.objects.get(id=corpus_file_id)
    corpus_file.get_and_save_summary()
    corpus_file.get_and_save_vector_of_summary()


@shared_task
def split_file_task(corpus_file_id: str) -> None:
    corpus_file = CorpusTextFile.objects.get(id=corpus_file_id)
    splits = corpus_file.split_content()
    for split in splits:
        # no need to chain
        generate_vector_task.delay(split.id)
        # generate_colbert_vectors_task.delay(split.id)


@shared_task
def generate_vector_task(split_id: str) -> None:
    split = Split.objects.get(id=split_id)
    split.get_and_save_vector()


# @shared_task
# def generate_colbert_vectors_task(split_id: str) -> None:
#     split = Split.objects.get(id=split_id)
#     split.get_and_save_colbert_vectors()


@shared_task
def simple_task():
    return "Simple task completed!"
