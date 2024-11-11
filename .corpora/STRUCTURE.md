This repository is structured as a polyglot monorepo, focused on Python. The organization prioritizes modularity and scalability.

- **py/**: Core Python codebase.
  - **packages/**: Primary location for Python packages, set as PYTHONPATH.
    - **corpora/**: Core library for managing corpora-related functionality.
    - **corpora_cli/**: Command-line interface tools.
    - **corpora_client/**: Client API for external interactions.
    - **corpora_proj/**: Project configuration and Django setup.
    - **corpora_ai/**: AI-related utilities and modules.
    - **corpora_pm/**: Project management integration.
  - **requirements.txt**: Python dependencies.
  - **requirements-dev.txt**: Development dependencies.
  - **pyproject.toml, pytest.ini**: Python packaging and testing configuration.

- **.devcontainer/**: Configurations for the development container setup.

- **.github/workflows/**: GitHub Actions workflows for CI/CD.

- **.corpora/**: Repository-specific metadata and guidelines.

- **docker/**: Docker configurations for deployment and testing environments.

This structure facilitates efficient development and deployment, emphasizing a scalable foundation for future growth.