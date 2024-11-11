from typing import List
from ninja import Router, Schema
from asgiref.sync import sync_to_async

from corpora_ai.llm_interface import ChatCompletionTextMessage
from corpora_ai.provider_loader import load_llm_provider
from corpora.models import Corpus

from ..auth import BearerAuth

workon_router = Router(tags=["workon"], auth=BearerAuth())


class MessageSchema(Schema):
    role: str  # e.g., "user", "system", "assistant"
    text: str


class CorpusFileChatSchema(Schema):
    corpus_id: str
    messages: List[MessageSchema]
    path: str
    # optional additional context: voice, purpose, structure, directions
    voice: str = ""
    purpose: str = ""
    structure: str = ""
    directions: str = ""


FILE_EDITOR_SYSTEM_MESSAGE = (
    "You are editing the file and must return only the new revision of the file. "
    "Do not include any additional context, explanations, or surrounding text. "
    "The output should only contain the file content."
)


class FileRevisionResponse(Schema):
    new_file_revision: str


def get_additional_context(payload: CorpusFileChatSchema) -> str:
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
        ext = payload.path.split(".")[-1]
        context += f"DIRECTIONS for {ext} filetype:\n\n{payload.directions}\n\n"

    return context


@workon_router.post("/file", response=str, operation_id="file")
async def file(request, payload: CorpusFileChatSchema):
    corpus = await Corpus.objects.aget(id=payload.corpus_id)

    # TODO: last 2 messages? Eventually we need to worry about
    # token count limits.
    # Ideally we might roll-up a summary of the entire conversation.
    # But, in the current design, we let the client decide the messages.
    # A separate endpoint could be used by the client to "compress conversation"
    split_context = await sync_to_async(corpus.get_relevant_splits_context)(
        "\n".join(message.text for message in payload.messages[-2:])
    )

    print(payload.messages[-1].text)

    all_messages = [
        ChatCompletionTextMessage(
            role="system",
            text=f"You are focused on the file: {payload.path} "
            f"in the {corpus.name} corpus. "
            f"{FILE_EDITOR_SYSTEM_MESSAGE}"
            f"{get_additional_context(payload)}",
        ),
        # Alternatively we use multiple system messages?
        # ChatCompletionTextMessage(role="system", text=VOICE_TEXT),
        # .corpora/VOICE.md
        # .corpora/PURPOSE.md
        # .corpora/STRUCTURE.md
        # .corpora/{ext}/DIRECTIONS.md
        ChatCompletionTextMessage(
            role="user",
            text=(
                f"I searched the broader corpus and found the following context:\n"
                f"---\n{split_context}\n---"
            ),
        ),
        *[
            ChatCompletionTextMessage(role=msg.role, text=msg.text)
            for msg in payload.messages
        ],
    ]

    llm = load_llm_provider()
    resp = llm.get_data_completion(all_messages, FileRevisionResponse)
    return resp.new_file_revision
