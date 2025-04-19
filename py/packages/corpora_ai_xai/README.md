# corpora_ai_xai

`corpora_ai_xai` provides an XAI implementation of the abstract interfaces defined in `corpora_ai`. It enables seamless use of XAI's API for generating text completions and embeddings within the Corpora framework.

## Features

- **Text Completion**: Generate natural language responses using XAI's chat models.

No text embedding support is available yet from XAI.

## Usage

### Initialization

Ensure `XAI_API_KEY` is set in your environment. Then, load the XAI client via `load_llm_provider`:

```python
from corpora_ai.provider_loader import load_llm_provider

# Load XAI client dynamically
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

## Requirements

- Set `LLM_PROVIDER=xai` and `XAI_API_KEY` in your environment.

For more details on provider selection, see `corpora_ai` documentation.
