# Base Image
FROM mcr.microsoft.com/devcontainers/python:3.12

# Install necessary system tools and dependencies
RUN apt-get update && \
    apt-get install -y \
        postgresql-client \
        zsh \
        wget \
        npm \
        openjdk-17-jre \
        redis-tools \
        docker-compose \
        build-essential \
        git \
        libffi-dev \
        python3-dev \
        && rm -rf /var/lib/apt/lists/*

# Set up the workspace and install Python dependencies
WORKDIR /workspace
COPY py/requirements.txt /workspace/requirements.txt
COPY py/requirements-dev.txt /workspace/requirements-dev.txt
COPY py/packages/corpora_proj/requirements.txt /workspace/packages/corpora_proj/requirements.txt
COPY py/packages/corpora/requirements.txt /workspace/packages/corpora/requirements.txt
COPY py/packages/corpora_cli/requirements.txt /workspace/packages/corpora_cli/requirements.txt
COPY py/packages/corpora_client/requirements.txt /workspace/packages/corpora_client/requirements.txt
COPY py/packages/corpora_client/test-requirements.txt /workspace/packages/corpora_client/test-requirements.txt
COPY py/packages/corpora_ai_openai/requirements.txt /workspace/packages/corpora_ai_openai/requirements.txt
RUN pip install --no-cache-dir -r /workspace/requirements.txt

CMD ["python", "manage.py", "runserver", "0.0.0.0:8877"]
