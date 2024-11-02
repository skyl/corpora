from typing import List
import uuid

from ninja import Router, Form, File
from ninja.files import UploadedFile
from asgiref.sync import sync_to_async

from .lib.files import calculate_checksum
from .lib.dj.decorators import async_raise_not_found
from .models import Corpus, File as CorpusFile
from .schema import CorpusSchema, CorpusResponseSchema, FileSchema, FileResponseSchema
from .auth import BearerAuth
from .tasks import process_tarball


api = Router(tags=["corpora"], auth=BearerAuth())


@api.post("/corpus", response={201: CorpusResponseSchema})
async def create_corpus(
    request,
    corpus: CorpusSchema = Form(...),
    tarball: UploadedFile = File(...),
):
    """Create a new Corpus with an uploaded tarball."""

    # Read tarball content and calculate checksum (for now, defer processing of individual files)
    # maybe we just add the whole file to `process_tarball`
    tarball_content: bytes = await sync_to_async(tarball.read)()

    print(f"Received tarball: {len(tarball_content)} bytes")

    # Create the corpus instance
    # TODO: validate unique name .. or ... init/sync ...
    # return 4XX and tell the client to try sync instead of init?
    corpus_instance = await Corpus.objects.acreate(
        name=corpus.name,
        url=corpus.url,
        owner=request.user,
        # TODO: what to do with the tarball?
        # tarball=tarball_content,  # Store tarball as-is for now
        # tarball_checksum=checksum,
    )
    process_tarball.delay(tarball_content)

    # Return the created corpus, automatically serialized by `CorpusResponseSchema`
    return corpus_instance


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
    checksum = calculate_checksum(payload.content)
    file = await CorpusFile.objects.acreate(
        path=payload.path, content=payload.content, checksum=checksum, corpus=corpus
    )
    return file


@api.get("/file/{file_id}", response=FileResponseSchema)
@async_raise_not_found
async def get_file(request, file_id: uuid.UUID):
    """Retrieve a File by ID."""
    file = await CorpusFile.objects.select_related("corpus").aget(id=file_id)
    return file
