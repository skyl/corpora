import uuid
from ninja import NinjaAPI
from corpora.lib.files import calculate_checksum
from corpora.lib.dj.decorators import async_raise_not_found
from .models import Corpus, File
from .schema import CorpusSchema, CorpusResponseSchema, FileSchema, FileResponseSchema

api = NinjaAPI()


@api.post("/corpus", response={201: CorpusResponseSchema})
async def create_corpus(request, payload: CorpusSchema):
    """Create a new Corpus."""
    corpus = await Corpus.objects.acreate(name=payload.name, url=payload.url)
    return corpus


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
    file = await File.objects.acreate(
        path=payload.path, content=payload.content, checksum=checksum, corpus=corpus
    )
    return file


@api.get("/file/{file_id}", response=FileResponseSchema)
@async_raise_not_found
async def get_file(request, file_id: uuid.UUID):
    """Retrieve a File by ID."""
    file = await File.objects.select_related("corpus").aget(id=file_id)
    return file
