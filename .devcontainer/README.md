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

2. **Create `.env` from Example:**
   - Copy `.env.example` to `.env`:
     
     ```bash
     cp .env.example .env
     ```

3. **Open in VS Code:**
   - Open the `corpora` folder in VS Code.
   - Ensure Docker is running.

4. **Build & Connect in DevContainer:**
   - Trigger the build process by reopening the folder in a container:
     - Open the Command Palette (Cmd+Shift+P or Ctrl+Shift+P).
     - Run `Remote-Containers: Reopen in Container`.

5. **Environment Configuration:**
   - **Set up API keys and credentials in `.env`:**
     
     ```
     OPENAI_API_KEY=""
     CORPORA_CLIENT_ID=""
     CORPORA_CLIENT_SECRET=""
     GITHUB_TOKEN=""
     ```

6. **Post-Setup Commands:**
   - Run server initialization commands:

     ```bash
     cd py/packages/corpora_proj
     ./manage.py migrate
     ./manage.py createsuperuser
     ```
   - Open your host browser and go to `localhost:8877/admin/`.
     - Log in with your superuser account.
     - Create an OAuth application:
       - URL: `http://localhost:8877/admin/oauth2_provider/application/add/`
       - Choose `Confidential` and `Client credentials`
       - Add your superuser as the owner of the application
       - Update `.env` file with `CORPORA_CLIENT_ID` and `CORPORA_CLIENT_SECRET`.

7. **Rebuild DevContainer:**
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
- **App:** 8877
- **Database:** 5432

## Notes
- Zsh customizations and Git configurations persist across sessions. All dependencies are managed within the container, ensuring a consistent development setup.