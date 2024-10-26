# Use a Python base image
FROM mcr.microsoft.com/devcontainers/python:3.12

# Install PostgreSQL client and Zsh
RUN apt-get update && apt-get install -y \
    postgresql-client zsh && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set up the workspace and install Python dependencies
WORKDIR /workspace
COPY py/ /workspace/py/
RUN pip install -r /workspace/py/requirements.txt
