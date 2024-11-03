from typing import List
import uuid

from django.db import IntegrityError
from django.core.exceptions import ValidationError
from ninja import Router, Form, File
from ninja.files import UploadedFile
from ninja.errors import HttpError

from asgiref.sync import sync_to_async

from .lib.files import compute_checksum
from .lib.dj.decorators import async_raise_not_found
from .models import Corpus, CorpusTextFile
from .schema import CorpusSchema, CorpusResponseSchema, FileSchema, FileResponseSchema
from .auth import BearerAuth
from .tasks import process_tarball


api = Router(tags=["corpora"], auth=BearerAuth())


@api.post("/corpus", response={201: CorpusResponseSchema, 400: str, 409: str})
async def create_corpus(
    request,
    corpus: CorpusSchema = Form(...),
    tarball: UploadedFile = File(...),
):
    """Create a new Corpus with an uploaded tarball."""

    # Read the tarball content
    tarball_content: bytes = await sync_to_async(tarball.read)()
    print(f"Received tarball: {len(tarball_content)} bytes")

    try:
        # Attempt to create the Corpus instance
        corpus_instance = await Corpus.objects.acreate(
            name=corpus.name,
            url=corpus.url,
            owner=request.user,
        )

    except IntegrityError as e:
        # Handle unique constraint violations (name/owner combo)
        raise HttpError(
            409, "A corpus with this name already exists for this owner."
        ) from e

    except ValidationError as e:
        # Handle other model validation issues if any
        raise HttpError(400, "Invalid data provided.") from e

    # Task creation to process the tarball asynchronously
    process_tarball.delay(str(corpus_instance.id), tarball_content)

    # Return the created Corpus instance
    return 201, corpus_instance


@api.delete("/corpus", response={204: str, 404: str})
@async_raise_not_found
async def delete_corpus(request, corpus_name: str):
    """Delete a Corpus by ID."""
    corpus = await Corpus.objects.aget(owner=request.user, name=corpus_name)
    await sync_to_async(corpus.delete)()
    return 204, "Corpus deleted."


@api.get("/corpus", response={200: List[CorpusResponseSchema]})
async def list_corpora(request):
    """List all Corpora."""
    # TODO .. pagination .. ?
    corpora = await sync_to_async(list)(Corpus.objects.filter(owner=request.user))
    return corpora


@api.get("/corpus/{corpus_id}", response=CorpusResponseSchema)
@async_raise_not_found
async def get_corpus(request, corpus_id: uuid.UUID):
    """Retrieve a Corpus by ID."""
    corpus = await Corpus.objects.aget(id=corpus_id)
    return corpus


@api.post("/file", response={201: FileResponseSchema})
@async_raise_not_found
async def create_file(request, payload: FileSchema):
    """Create a new File within a Corpus."""
    corpus = await Corpus.objects.aget(id=payload.corpus_id)
    checksum = compute_checksum(payload.content)
    file = await CorpusTextFile.objects.acreate(
        path=payload.path,
        content=payload.content,
        checksum=checksum,
        corpus=corpus,
    )
    return file


@api.get("/file/{file_id}", response=FileResponseSchema)
@async_raise_not_found
async def get_file(request, file_id: uuid.UUID):
    """Retrieve a File by ID."""
    file = await CorpusTextFile.objects.select_related("corpus").aget(id=file_id)
    return file
