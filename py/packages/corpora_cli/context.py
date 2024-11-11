from typing import Any, Dict
from dataclasses import dataclass
from rich.console import Console

from corpora_client import CorpusApi, FileApi, SplitApi, PlanApi, WorkonApi


@dataclass
class ContextObject:
    corpus_api: CorpusApi
    file_api: FileApi
    split_api: SplitApi
    plan_api: PlanApi
    workon_api: WorkonApi
    config: Dict[str, Any]
    console: Console
