from typing import List
from ninja import Schema


class MessageSchema(Schema):
    role: str  # e.g., "user", "system", "assistant"
    text: str


class CorpusChatSchema(Schema):
    corpus_id: str
    messages: List[MessageSchema]
    # optional additional context: voice, purpose, structure, directions
    voice: str = ""
    purpose: str = ""
    structure: str = ""
    directions: str = ""


class CorpusFileChatSchema(CorpusChatSchema):
    path: str


def get_additional_context(payload: CorpusChatSchema, ext: str = "") -> str:
    # TODO: more automatically expandable implementation
    # without the ifs
    context = ""
    if any(
        [
            payload.voice,
            payload.purpose,
            payload.structure,
            payload.directions,
        ]
    ):
        context += "\n\nADDITIONAL CONTEXT:\n\n"

    if payload.voice:
        context += f"VOICE:\n\n{payload.voice}\n\n"

    if payload.purpose:
        context += f"PURPOSE of corpus:\n\n{payload.purpose}\n\n"

    if payload.structure:
        context += f"STRUCTURE of corpus:\n\n{payload.structure}\n\n"

    if payload.directions:
        context += f"DIRECTIONS for {ext} filetype:\n\n{payload.directions}\n\n"

    return context
