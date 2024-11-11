from typing import List
from ninja import Router, Schema
from asgiref.sync import sync_to_async
from regex import F

from corpora_ai.llm_interface import ChatCompletionTextMessage
from corpora_ai.provider_loader import load_llm_provider
from corpora.models import Corpus

from ..auth import BearerAuth

workon_router = Router(tags=["workon"], auth=BearerAuth())


# # TODO: get this from configuration
# VOICE_TEXT = """
# You are concise. You use minimal language. Less is more. This isn't a marketing pitch.
# """


# TODO: DRY!!!


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


FILE_EDITOR_SYSTEM_MESSAGE = "You return the new revision of the file."


@workon_router.post("/file", response=str, operation_id="get_revision")
async def file(request, payload: CorpusFileChatSchema):
    corpus = await Corpus.objects.aget(id=payload.corpus_id)

    split_context = await sync_to_async(corpus.get_relevant_splits_context)(
        "\n".join(message for message in payload.messages[-2:])
    )

    all_messages = [
        ChatCompletionTextMessage(
            role="system",
            text=f"You are focused on the file: {payload.path} "
            "in the {corpus.name} corpus. "
            "{FILE_EDITOR_SYSTEM_MESSAGE}"
            f"{payload.voice}\n{payload.purpose}\n{payload.structure}\n{payload.directions}",
        ),
        # ChatCompletionTextMessage(role="system", text=VOICE_TEXT),
        # .corpora/VOICE.md
        # .corpora/PURPOSE.md
        # .corpora/STRUCTURE.md
        # .corpora/{ext}/DIRECTIONS.md
        ChatCompletionTextMessage(
            role="user",
            text=f"I searched the broader corpus and found the following context:\n"
            f"---\n{split_context}\n---",
        ),
        *[
            ChatCompletionTextMessage(role=msg.role, text=msg.text)
            for msg in payload.messages
        ],
    ]

    llm = load_llm_provider()
    resp = llm.get_text_completion(all_messages)
    return resp
