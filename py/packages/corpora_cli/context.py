from dataclasses import dataclass
from rich.console import Console
from corpora_client import CorpusApi, FileApi, SplitApi, PlanApi
from typing import Dict, Any


@dataclass
class ContextObject:
    corpus_api: CorpusApi
    file_api: FileApi
    split_api: SplitApi
    plan_api: PlanApi
    config: Dict[str, Any]
    console: Console
