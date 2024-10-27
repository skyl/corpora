# Corpora DevContainer

This DevContainer setup provides a ready-to-use development environment with Docker Compose, Python 3.12, PostgreSQL, and zsh.

## Features
- **Python 3.12** with dependencies installed from `requirements.txt`
- **PostgreSQL** service with environment variables for connection configuration
- **Zsh** shell with custom history and useful aliases
- **VS Code Customizations** for Python linting, formatting, and Docker integration

## Usage
1. **Open in VS Code:** Open this folder in VS Code, ensuring Docker is running.
2. **Build & Connect:** The DevContainer will automatically build and connect to VS Code.
3. **Run Commands:** Post-create setup (`setup.sh`) installs Zsh customizations.

## Ports
- **App:** 8000
- **Database:** 5432

## Notes
- zsh customizations and Git configuration are persisted across sessions.
