from dataclasses import dataclass
from rich.console import Console
from corpora_client import CorpusApi, FilesApi, SplitsApi
from typing import Dict, Any


@dataclass
class ContextObject:
    corpus_api: CorpusApi
    files_api: FilesApi
    splits_api: SplitsApi
    config: Dict[str, Any]
    console: Console
