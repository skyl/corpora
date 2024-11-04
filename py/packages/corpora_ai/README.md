# corpora_ai

`corpora_ai` is an abstraction layer for interacting with various Large Language Model (LLM) providers. It provides a unified API for generating text completions and embeddings, allowing seamless switching between providers.

## Overview

- **Provider-Agnostic Interface**: Define LLM capabilities with a single, standardized API.
- **Dynamic Provider Loading**: Select the best available LLM provider based on environment variables.
- **Modular**: Built to support provider-specific implementations (e.g., `corpora_ai_openai`), each loaded as needed.

## Usage

To use the default OpenAI provider, simply set the `OPENAI_API_KEY` environment variable.

```bash

### Loading an LLM Provider

```python
from corpora_ai.provider_loader import load_llm_provider

# Dynamically load the configured LLM provider
llm = load_llm_provider()
```

### Generating a Completion

```python
from corpora_ai.llm_interface import ChatCompletionTextMessage

messages = [ChatCompletionTextMessage(role="user", content="Tell me a joke.")]
response = llm.get_text_completion(messages)
print(response)
```

### Generating an Embedding

```python
embedding = llm.get_embedding("Sample text for embedding")
print(embedding)
```
