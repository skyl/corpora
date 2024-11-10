from typing import List
from ninja import Router, Schema
from asgiref.sync import sync_to_async

from corpora_ai.llm_interface import ChatCompletionTextMessage
from corpora_ai.provider_loader import load_llm_provider
from corpora.auth import BearerAuth
from corpora.models import Corpus


ISSUE_MAKER_SYSTEM_MESSAGE = (
    "You are a highly skilled assistant specializing in creating well-structured, actionable issues "
    "for this project. Your goal is to process the provided context and user input to generate "
    "a concise and clear issue. This issue should include an informative title and a detailed body, "
    "providing contributors with the necessary insights to effectively address the task. "
    "Highlight relevant sections of the corpus and ensure that the issue is easy to understand and work on. "
)


class IssueSchema(Schema):
    title: str
    body: str


class MessageSchema(Schema):
    role: str  # e.g., "user", "system", "assistant"
    text: str


class IssueRequestSchema(Schema):
    corpus_id: str
    messages: List[MessageSchema]


plan_router = Router(tags=["plan"], auth=BearerAuth())


@plan_router.post("/issue", response=IssueSchema, operation_id="get_issue")
async def get_issue(request, payload: IssueRequestSchema):
    corpus = await Corpus.objects.aget(id=payload.corpus_id)

    # TODO: split context could be ... ?
    split_context = await sync_to_async(corpus.get_relevant_splits_context)(
        payload.messages[-1].text
    )

    print(split_context)

    all_messages = [
        ChatCompletionTextMessage(role="system", text=ISSUE_MAKER_SYSTEM_MESSAGE),
        ChatCompletionTextMessage(
            role="user",
            text=f"---\nI searched and found the following in the existing context that may be helpful:\n\n"
            f"{split_context}\n"
            "---\n",
        ),
        *[
            ChatCompletionTextMessage(role=msg.role, text=msg.text)
            for msg in payload.messages
        ],
    ]

    llm = load_llm_provider()
    resp = llm.get_data_completion(all_messages, IssueSchema)
    return resp
