from typing import List
import uuid

from ninja import Router
from pgvector.django import CosineDistance
from asgiref.sync import sync_to_async

from ..models import Split
from ..schema import SplitResponseSchema, SplitVectorSearchSchema
from ..auth import BearerAuth

split_router = Router(tags=["splits"], auth=BearerAuth())


@split_router.post("/search", response=List[SplitResponseSchema])
async def vector_search_splits(request, payload: SplitVectorSearchSchema):
    """Perform a vector similarity search for splits using a provided query vector."""
    query_vector = payload.vector
    corpus_id = payload.corpus_id

    # Using cosine similarity for the search
    similar_splits = await sync_to_async(list)(
        Split.objects.filter(
            vector__isnull=False,
            file__corpus_id=corpus_id,
        )
        .annotate(similarity=CosineDistance("vector", query_vector))
        .order_by("similarity")[: payload.limit]
    )

    return similar_splits


@split_router.get("/{split_id}", response=SplitResponseSchema)
async def get_split(request, split_id: uuid.UUID):
    """Retrieve a Split by ID."""
    split = await Split.objects.select_related("file", "file__corpus").aget(id=split_id)
    return split


@split_router.get("/file/{file_id}", response=List[SplitResponseSchema])
async def list_splits_for_file(request, file_id: uuid.UUID):
    """List all Splits for a specific CorpusTextFile."""
    splits = await sync_to_async(list)(
        Split.objects.filter(file_id=file_id).order_by("order")
    )
    return splits
