import os
from typing import Optional
from corpora_ai.llm_interface import LLMBaseInterface

# Import provider-specific clients
try:
    from corpora_ai_openai.llm_client import OpenAIClient
except ImportError:
    OpenAIClient = None  # This handles cases where the OpenAI client isn't installed

# Future imports for other providers, e.g., Anthropic or Cohere, would follow the same pattern


def load_llm_provider() -> Optional[LLMBaseInterface]:
    """
    Dynamically loads the best LLM provider based on environment variables.

    Returns:
        Optional[LLMBaseInterface]: An instance of the best available LLM provider.
    """
    provider_name = os.getenv("LLM_PROVIDER", "openai")

    # Check for the OpenAI provider
    if provider_name == "openai" and OpenAIClient:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set.")
        return OpenAIClient(api_key=api_key)

    # Placeholder for additional providers (e.g., Anthropic)
    # elif provider_name == "anthropic" and AnthropicClient:
    #     return AnthropicClient(api_key=os.getenv("ANTHROPIC_API_KEY"))

    raise ValueError("No valid LLM provider found.")
