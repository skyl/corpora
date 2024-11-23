from datetime import datetime
from typing import Optional
from uuid import UUID

from ninja import Schema


class CorpusSchema(Schema):
    name: str
    url: Optional[str] = None


class CorpusResponseSchema(Schema):
    id: UUID
    name: str
    url: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class FileSchema(Schema):
    path: str
    content: str
    corpus_id: UUID


class FileResponseSchema(Schema):
    id: UUID
    corpus_id: UUID
    path: str
    content: str
    checksum: str
    created_at: datetime
    updated_at: datetime


class SplitVectorSearchSchema(Schema):
    corpus_id: UUID
    text: str
    limit: int = 10


class SplitResponseSchema(Schema):
    id: UUID
    content: str
    order: int
    file_id: UUID
    # vector: List[float] = None
