from re import I
from ninja import Router

# TODO
# These can be used on the CLI side
# from corpora_pm.abstract import Issue
# from corpora_pm.providers.provider_loader import load_provider
# provider is just for if we want to actually post it :thinking:
# maybe this can be done on the CLI-side actually
# provider = load_provider(corpus)
# The purpose here is to return a prospective issue based on the text
# we will search the corpus, look at general context and return
# the issue to the caller. The caller can then decide to post it
# or they can give further instructions.

from corpora_ai.llm_interface import ChatCompletionTextMessage
from corpora_ai.provider_loader import load_llm_provider

from corpora.auth import BearerAuth
from corpora.models import Corpus

from ninja import Schema


ISSUE_MAKER_SYSTEM_MESSAGE = (
    "You are an expert at creating issues for this project. "
    "You can take a large amount of context and distill it into a concise issue. "
    "That will be clear for a contributor to understand and work on. "
    "You provide insight into what parts of the corpus the user will be interested in. "
)


class IssueSchema(Schema):
    title: str
    body: str


split_router = Router(tags=["split"], auth=BearerAuth())


# Given a corpus_id and some text (rough description of issue),
# return a prospective issue
@split_router.post("/{corpus_id}/issue", response=IssueSchema, operation_id="get_issue")
async def get_issue(request, corpus_id: str, text: str):
    corpus = await Corpus.objects.aget(id=corpus_id)
    splits = corpus.get_relevant_splits(text)

    # TODO: this should maybe be part of the provider?
    # it could be like get_issue ... but maybe it could be abstract
    # for any passed schema? That would be hot:
    # get_data_completion(Messages, Schema) -> Schema
    # oooo
    split_context = ""
    for split in splits:
        split_context += f"{split.file.path}\n```\n{split.content}\n```"

    llm = load_llm_provider()
    resp = llm.get_data_completion(
        [
            ChatCompletionTextMessage(role="system", text=ISSUE_MAKER_SYSTEM_MESSAGE),
            ChatCompletionTextMessage(role="context", text=split_context),
            ChatCompletionTextMessage(role="user", text=text),
        ],
        IssueSchema,
    )
    return resp
