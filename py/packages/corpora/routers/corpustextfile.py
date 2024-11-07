import uuid

from django.db import IntegrityError
from ninja import Router
from ninja.errors import HttpError

from ..lib.files import compute_checksum
from ..lib.dj.decorators import async_raise_not_found
from ..models import Corpus, CorpusTextFile
from ..schema import FileSchema, FileResponseSchema
from ..auth import BearerAuth

file_router = Router(tags=["file"], auth=BearerAuth())


@file_router.post(
    "", response={201: FileResponseSchema, 409: str}, operation_id="create_file"
)
@async_raise_not_found
async def create_file(request, payload: FileSchema):
    """Create a new File within a Corpus."""
    corpus = await Corpus.objects.aget(id=payload.corpus_id)
    checksum = compute_checksum(payload.content)
    try:
        file = await CorpusTextFile.objects.acreate(
            path=payload.path,
            content=payload.content,
            checksum=checksum,
            corpus=corpus,
        )
    except IntegrityError:
        # Handle the unique constraint violation for duplicate file paths within the same corpus
        raise HttpError(409, "A file with this path already exists in the corpus.")

    return 201, file


@file_router.get("/{file_id}", response=FileResponseSchema, operation_id="get_file")
@async_raise_not_found
async def get_file(request, file_id: uuid.UUID):
    """Retrieve a File by ID."""
    file = await CorpusTextFile.objects.select_related("corpus").aget(id=file_id)
    return file
