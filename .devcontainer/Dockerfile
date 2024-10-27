FROM mcr.microsoft.com/devcontainers/python:3.12

# Install PostgreSQL client and zsh
RUN apt-get update && apt-get install -y \
    postgresql-client zsh && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set up the workspace
WORKDIR /workspace

# Create necessary directories before copying requirements files
RUN mkdir -p /workspace/packages/corpora

# Copy individual requirements files, preserving paths
COPY py/requirements.txt /workspace/requirements.txt
COPY py/requirements-dev.txt /workspace/requirements-dev.txt
COPY py/packages/corpora/requirements.txt /workspace/packages/corpora/requirements.txt

# Install dependencies from all requirements files
RUN pip install --no-cache-dir -r /workspace/requirements.txt

# Copy the rest of the application
# COPY py/ /workspace/py/

# Set default shell to zsh for the "vscode" user
RUN chsh -s /bin/zsh vscode

# Run zsh as the main process in interactive mode
CMD ["sleep", "infinity"]
