from asgiref.sync import sync_to_async
from corpora_ai.llm_interface import ChatCompletionTextMessage
from corpora_ai.provider_loader import load_llm_provider
from ninja import Router, Schema

from corpora.auth import BearerAuth
from corpora.models import Corpus
from corpora.schema.chat import CorpusChatSchema, get_additional_context

ISSUE_MAKER_SYSTEM_MESSAGE = (
    "You are a skilled assistant focused on creating clear, actionable issues for this project. "
    "Your task is to analyze the provided context and user input to generate a concise issue. "
    "Each issue must include: "
    "- A clear, informative title. "
    "- A detailed body explaining the problem, goals, and relevant context. "
    "Provide contributors with sufficient information to address the task effectively. "
    "Avoid prescribing solutions; instead, outline viable options where relevant. "
    "Be terse and direct—this is a technical task, not a marketing pitch. "
    "Avoid unnecessary language and prioritize clarity and precision."
)


class IssueSchema(Schema):
    title: str
    body: str


plan_router = Router(tags=["plan"], auth=BearerAuth())


@plan_router.post("/issue", response=IssueSchema, operation_id="get_issue")
async def get_issue(request, payload: CorpusChatSchema):
    corpus = await Corpus.objects.aget(id=payload.corpus_id)

    # TODO: split context could be ... ?
    split_context = await sync_to_async(corpus.get_relevant_splits_context)(
        "\n".join(message.text for message in payload.messages[-2:]),
    )

    print(split_context)

    all_messages = [
        ChatCompletionTextMessage(
            role="system",
            text=f"{ISSUE_MAKER_SYSTEM_MESSAGE}{get_additional_context(payload)}",
        ),
        ChatCompletionTextMessage(
            role="user",
            text=f"---\n"
            f"I searched and found some file splits in the {corpus.name} corpus that may be helpful:\n\n"
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
