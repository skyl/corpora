# Corpora

Corpora is an experimental polyglot monorepo focused on creating tools to enhance and evolve textual corpora through AI integration, efficient data management, and automation processes.

## Key Components

- [**py/**](py/README.md): Contains core Python codebase, including modular packages and Django apps.
  - [**corpora_cli/**](py/packages/corpora_cli/README.md): Command-line tools for interacting with and managing corpora.
  - [**corpora_proj/**](py/packages/corpora_proj/README.md): Django project for testing and development with a Ninja API.
  - [**corpora/**](py/packages/corpora/README.md): Core library for managing textual data.

- [**.devcontainer/**](.devcontainer/README.md): Provides a development environment with Docker, allowing easy setup for contributors and users.

## Philosophy and Goals

Our aim is to create a flexible system for managing text corpora that provides comprehensive AI-driven insights and metadata generation. By integrating interfaces to AI models and project management tools, we enhance developer workflows and decision-making. The repository is structured to facilitate easy expansion and integration with various AI and project management platforms such as OpenAI and GitHub, with plans for future adaptability to other services like GitLab.

## Contributing

Clone the repository and open it in a devcontainer, which provides a full setup with a running server, CLI, PostgreSQL, Redis, and Celery. This allows you to begin developing and utilizing Corpora immediately. Use the tools and structure to contribute enhancements or support new features that align with these goals.

Licensed under AGPL, Corpora can be used within your company to aid in proprietary codebase development, with the requirement that modifications are open-sourced.