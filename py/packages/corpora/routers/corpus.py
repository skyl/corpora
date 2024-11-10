from typing import Dict, List
import uuid

from django.db import IntegrityError
from django.core.exceptions import ValidationError
from ninja import Router, Form, File
from ninja.files import UploadedFile
from ninja.errors import HttpError
from asgiref.sync import sync_to_async

from ..auth import BearerAuth
from ..lib.dj.decorators import async_raise_not_found
from ..models import Corpus
from ..schema import CorpusSchema, CorpusResponseSchema
from ..tasks import process_tarball

corpus_router = Router(tags=["corpus"], auth=BearerAuth())


@corpus_router.post(
    "",
    response={201: CorpusResponseSchema, 400: str, 409: str},
    operation_id="create_corpus",
)
async def create_corpus(
    request,
    corpus: CorpusSchema = Form(...),
    tarball: UploadedFile = File(...),
):
    """Create a new Corpus with an uploaded tarball."""
    tarball_content: bytes = await sync_to_async(tarball.read)()
    try:
        corpus_instance = await Corpus.objects.acreate(
            name=corpus.name,
            url=corpus.url,
            owner=request.user,
        )
    except IntegrityError:
        raise HttpError(409, "A corpus with this name already exists for this owner.")
    except ValidationError:
        raise HttpError(400, "Invalid data provided.")

    process_tarball.delay(str(corpus_instance.id), tarball_content)
    return 201, corpus_instance


# get_file_hashes will return a map of file paths to their hashes from the database
@corpus_router.get(
    "/{corpus_id}/files", response=Dict[str, str], operation_id="get_file_hashes"
)
async def get_file_hashes(request, corpus_id: uuid.UUID):
    """Retrieve a map of file paths to their hashes for a Corpus."""
    corpus = await Corpus.objects.aget(id=corpus_id)
    return await sync_to_async(corpus.get_file_hashes)()


@corpus_router.delete("", response={204: str, 404: str}, operation_id="delete_corpus")
@async_raise_not_found
async def delete_corpus(request, corpus_name: str):
    """Delete a Corpus by name."""
    corpus = await Corpus.objects.aget(owner=request.user, name=corpus_name)
    await sync_to_async(corpus.delete)()
    return 204, "Corpus deleted."


@corpus_router.get(
    "", response={200: List[CorpusResponseSchema]}, operation_id="list_corpora"
)
async def list_corpora(request):
    """List all Corpora."""
    corpora = await sync_to_async(list)(Corpus.objects.filter(owner=request.user))
    return corpora


@corpus_router.get(
    "/{corpus_id}", response=CorpusResponseSchema, operation_id="get_corpus"
)
@async_raise_not_found
async def get_corpus(request, corpus_id: uuid.UUID):
    """Retrieve a Corpus by ID."""
    corpus = await Corpus.objects.aget(id=corpus_id)
    return corpus
