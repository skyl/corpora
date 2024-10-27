# packages/corpora/conftest.py
import pytest
from httpx import AsyncClient
from .api import api


@pytest.fixture
def client():
    """Sets up the test client for NinjaAPI."""
    return AsyncClient(app=api, base_url="http://testserver")
