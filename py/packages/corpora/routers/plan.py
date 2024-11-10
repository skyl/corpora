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


plan_router = Router(tags=["plan"], auth=BearerAuth())


# Given a corpus_id and some text (rough description of issue),
# return a prospective issue
@plan_router.post("/{corpus_id}/issue", response=IssueSchema, operation_id="get_issue")
async def get_issue(request, corpus_id: str, text: str):
    corpus = await Corpus.objects.aget(id=corpus_id)
    # split_context = corpus.get_relevant_splits_context(text)
    split_context = await sync_to_async(corpus.get_relevant_splits_context)(text)
    print(split_context)

    llm = load_llm_provider()
    resp = llm.get_data_completion(
        [
            ChatCompletionTextMessage(role="system", text=ISSUE_MAKER_SYSTEM_MESSAGE),
            # RuntimeError: Failed to generate data completion: Error code: 400 - {'error':
            # {'message': "Invalid value: 'context'. Supported values are: 'system',
            # 'assistant', 'user', 'function', and 'tool'.", 'type': 'invalid_request_error',
            # 'param': 'messages[1].role', 'code': 'invalid_value'}}
            # ChatCompletionTextMessage(role="context", text=split_context),
            ChatCompletionTextMessage(
                role="user",
                text=f"---\nI searched and found the following in the existing context that may be helpful:\n\n```{split_context}\n```---\n",
            ),
            ChatCompletionTextMessage(role="user", text=text),
        ],
        IssueSchema,
    )
    return resp
