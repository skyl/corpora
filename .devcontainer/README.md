# Corpora DevContainer

This DevContainer setup provides a development environment with Docker Compose, Python 3.12, PostgreSQL, Rust, and zsh.

## Features
- **Python 3.12** with dependencies from `requirements.txt`
- **PostgreSQL** service with configurable environment variables
- **Rust/Cargo** integrated for additional development
- **VS Code Customizations** for Python linting, formatting, and Docker integration

## Prerequisites
- Docker
- Visual Studio Code

## Quick Setup
1. **Clone the Repository:**
   
   ```bash
   git clone https://github.com/skyl/corpora.git
   cd corpora
   ```

2. **Create `.env` from Example:**
   - Copy `.env.example` to `.env`:
     
     ```bash
     cp .env.example .env
     ```

3. **Open in VS Code:**
   - Open the `corpora` folder in VS Code.
   - Ensure Docker is running.

4. **Build & Connect in DevContainer:**
   - Reopen the folder in a container:
     - Open Command Palette (Cmd+Shift+P or Ctrl+Shift+P).
     - Run `Remote-Containers: Reopen in Container`.

5. **Environment Configuration:**
   - **Set API keys and credentials in `.env`:**
     
     ```
     OPENAI_API_KEY=""
     CORPORA_CLIENT_ID=""
     CORPORA_CLIENT_SECRET=""
     GITHUB_TOKEN=""
     ```

6. **Post-Setup Commands:**
   - Run server initialization:

     ```bash
     cd py/packages/corpora_proj
     ./manage.py migrate
     ./manage.py createsuperuser
     ```
   - Access at `localhost:8877/admin/` to set up OAuth.

7. **Rebuild DevContainer:**
   - Reload to apply `.env` changes.

## Usage Example

With `.env` configured and the devcontainer running, use CLI commands:

```bash
corpora corpus init
corpora corpus sync
corpora workon file README.md
corpora plan issue
```

## Ports
- **App:** 8877
- **Database:** 5432

## Notes
- Variations in Docker setup can be found in `../docker-compose.yaml` and `../docker/README.md`.
- To run without VS Code, use Docker Compose directly.
- The directory sets up Docker and Compose for VS Code integration.
- Contains `README.md`, `devcontainer.json`, `setup.sh`.
- Interactive container includes Rust/Cargo, full Python/Django/Postgres setup, with zsh.