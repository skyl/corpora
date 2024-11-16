# Rust Workspace (rs)

This Rust workspace is designed for multipackage setups, facilitating scalable and modular development.

## Key Components

- **corpora_cli**: Currently serves as the executable in the workspace. Refer to [Cargo.toml](Cargo.toml) to understand workspace dependencies and configurations.

- **corpora_client**: OpenAPI generated client library. Run `genall.sh` to generate and verify code based on the API specification from [the corpora server](../py/packages/corpora_proj/README.md). Ensure that all generated outputs are verified and committed.

- **genall.sh**: Script used to regenerate `corpora_client`, format, and test the codebase.

## Development Workflow

- See the configuration details in `Cargo.toml` to understand package management.
- Check [GitHub Actions](../.github/workflows/README.md) for CI/CD workflows.
- Follow the [DevContainer Setup](../.devcontainer/README.md) for configuring the development environment.
