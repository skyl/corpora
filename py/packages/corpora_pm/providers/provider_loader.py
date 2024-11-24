# from corpora.models import Corpus

import uuid

from pydantic import BaseModel

from ..abstract import AbstractIssueTracker


class Corpus(BaseModel):
    url: str
    id: uuid.UUID


def load_provider(corpus: Corpus) -> AbstractIssueTracker:
    """Load an issue tracker provider for the given corpus.
    """
    # TODO: better way to determine provider
    # - support enterprise with custom URL
    if "github" in corpus.url:
        from .github.pm import GitHubIssueTracker

        return GitHubIssueTracker()

    raise NotImplementedError(f"Provider not implemented for {corpus.url}")
