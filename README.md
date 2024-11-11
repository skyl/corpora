# Corpora

> Corpora is a corpus of tools to enhance and evolve arbitrary corpora including itself.

Corpora is an experimental polyglot monorepo focused on creating tools to enhance and evolve textual corpora with AI. Our aim is to create a flexible systems for managing text corpora to increase contributor productivity.

## Key Components

- [**py/**](py/README.md): Contains core Python codebase, including modular packages and Django apps.
  - [**corpora_cli/**](py/packages/corpora_cli/README.md): Command-line tools for interacting with and managing corpora.
  - [**corpora_proj/**](py/packages/corpora_proj/README.md): Django project for testing and development with a Ninja API.
  - [**corpora/**](py/packages/corpora/README.md): Core library for managing textual data.

- [**.devcontainer/**](.devcontainer/README.md): Provides a development environment with Docker, allowing easy setup for contributors and users.

## Contributing

Clone the repository and open it in a devcontainer, which provides a full setup with a running server, CLI, PostgreSQL, Redis, and Celery. This allows you to begin developing and utilizing Corpora immediately. Use the tools and structure to contribute enhancements or support new features that align with these goals.

Licensed under AGPL, Corpora can be used within your company to aid in proprietary codebase development, with the requirement that modifications are open-sourced.