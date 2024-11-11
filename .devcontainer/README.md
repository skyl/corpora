# Corpora DevContainer

This DevContainer setup provides a ready-to-use development environment with Docker Compose, Python 3.12, PostgreSQL, and zsh.

## Features
- **Python 3.12** with dependencies installed from `requirements.txt`
- **PostgreSQL** service with environment variables for connection configuration
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

2. **Open in VS Code:**
   - Open the `corpora` folder in VS Code.
   - Ensure Docker is running.

3. **Build & Connect in DevContainer:**
   - Trigger the build process by reopening the folder in a container:
     - Open the Command Palette (Cmd+Shift+P or Ctrl+Shift+P).
     - Run `Remote-Containers: Reopen in Container`.

4. **Environment Configuration:**
   - **Set up `.env` file:**
     - Add your API keys and credentials:

     ```
     OPENAI_API_KEY=""
     CORPORA_CLIENT_ID=""
     CORPORA_CLIENT_SECRET=""
     GITHUB_TOKEN=""
     ```

5. **Post-Setup Commands:**
   - Run server initialization commands:

     ```bash
     cd py/packages/corpora_proj
     ./manage.py createsuperuser
     ```
   - Open your browser and go to `localhost:8000/admin/`.
     - Log in with your superuser account.
     - Create an OAuth application:
       - URL: `http://127.0.0.1:8000/admin/oauth2_provider/application/add/`
       - Choose `Confidential` and `Client credentials`.
       - Update `.env` file with `CORPORA_CLIENT_ID` and `CORPORA_CLIENT_SECRET`.

6. **Rebuild DevContainer:**
   - Reload the container to apply `.env` updates.

## Usage Example

With `.env` configured and the devcontainer running, use CLI commands from the project root:

```bash
corpora corpus init
corpora corpus sync
corpora workon file README.md
corpora plan issue
```

## Ports
- **App:** 8000
- **Database:** 5432

## Notes
- Zsh customizations and Git configurations persist across sessions. All dependencies are managed within the container, ensuring a consistent development setup.