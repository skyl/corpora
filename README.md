# Corpora

> Corpora is a corpus of tools to enhance and evolve arbitrary corpora including itself.

Corpora is an experimental polyglot monorepo focused on creating tools to enhance and evolve textual corpora with AI. Our aim is to create a flexible system for managing text corpora to increase contributor productivity.

## Key Components

- [**.corpora/**](.corpora/README.md): Repository-specific metadata and guidelines.
- [**.devcontainer/**](.devcontainer/README.md): Provides a development environment with Docker, allowing easy setup for contributors and users.
- [**.github/**](.github/README.md): GitHub Actions workflows for CI/CD.
- [**docker/**](docker/README.md): Docker configurations for deployment and testing environments.
- [**md/**](md/README.md): Documentation and notes.
- [**py/**](py/README.md): Contains core Python codebase, including modular packages and Django apps.
- [**rs/**](rs/README.md): Multipackage Rust workspace for extensible tool development.

## Contributing

Clone the repository and open it in a devcontainer, which provides a full setup with a running server, CLI, PostgreSQL, Redis, and Celery. This allows you to begin developing and utilizing Corpora immediately. Use the tools and structure to contribute enhancements or support new features that align with these goals.

Licensed under AGPL, Corpora can be used within your company to aid in proprietary codebase development, with the requirement that modifications are open-sourced.