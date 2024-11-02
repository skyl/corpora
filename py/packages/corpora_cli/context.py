from dataclasses import dataclass
from rich.console import Console
from corpora_client import CorporaApi
from typing import Dict, Any


@dataclass
class ContextObject:
    api_client: CorporaApi
    config: Dict[str, Any]
    console: Console
