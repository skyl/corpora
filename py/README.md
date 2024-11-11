# Python Codebase

Python code for **Corpora** — a tool suite for advancing arbitrary corpora.

## Overview

The `py/` directory contains the main Python codebase, comprising core packages and configurations:

- [**packages/**](packages/README.md): Modular Python packages.
- [**requirements.txt**](../requirements.txt): Aggregated global dependencies.
- [**requirements-dev.txt**](../requirements-dev.txt): Development-specific dependencies.

For modularity, each package has its own `requirements.txt`. The global `requirements.txt` can install all dependencies, yet the devcontainer pre-configures everything for you [Dockerfile](../.devcontainer/Dockerfile). Everything is ready out of the box within the devcontainer. Check the [DevContainer Setup](../.devcontainer/README.md) for an understanding of the pre-defined environment.

For trying new dependencies, you can simply use `pip` without further setup and add them to the respective `requirements.txt`. The devcontainer will automatically install them on the next build.

## Packages

- **corpora**: Core library for corpus management.
- **corpora_ai**: AI utilities, server-side integration.
- **corpora_ai_openai**: Extensions using OpenAI.
- **corpora_cli**: Command-line tools.
- **corpora_client**: API client, auto-generated.
- **corpora_pm**: Project management tools.
- **corpora_proj**: Django project setup, runs `corpora` app.

Each package serves a distinct purpose:

- **corpora** integrates with `pgvector` models and corpus data, acting as the RAG source for `corpora_ai`.
- **corpora_client** is generated from the server APIs, with `corpora_cli` utilizing the client for operations.
- **corpora_ai** facilitates server-side AI functionalities, allowing configurable server deployments.
- **corpora_pm** is CLI-focused, leveraging local `GITHUB_TOKEN` for Github operations, managed by `corpora_cli`.

## Development Workflow

- **API Development**: Add endpoints in `corpora`. Use `./genall.sh` to update `corpora_client` and `corpora_cli`.
- **Testing and Formatting**: Use `black` for code formatting and `pytest` for tests.
