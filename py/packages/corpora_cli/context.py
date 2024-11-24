from dataclasses import dataclass
from typing import Any, Dict

from corpora_client import CorpusApi, FileApi, PlanApi, SplitApi, WorkonApi
from rich.console import Console


@dataclass
class ContextObject:
    corpus_api: CorpusApi
    file_api: FileApi
    split_api: SplitApi
    plan_api: PlanApi
    workon_api: WorkonApi
    config: Dict[str, Any]
    console: Console
