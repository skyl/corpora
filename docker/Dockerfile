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

RUN npm install -g @openapitools/openapi-generator-cli && \
    sudo openapi-generator-cli version

# --------------------------------------------------------------------------
# Musl-linked Python and Static Compilation Setup
# --------------------------------------------------------------------------

# Install musl-tools and other build essentials
RUN apt-get update && \
    apt-get install -y \
        musl-tools \
        && rm -rf /var/lib/apt/lists/*

# Detect architecture and download the appropriate musl cross-compiler
RUN ARCH=$(uname -m) && \
    if [ "$ARCH" = "x86_64" ]; then \
        wget https://musl.cc/x86_64-linux-musl-cross.tgz -O musl-cross.tgz; \
    elif [ "$ARCH" = "aarch64" ]; then \
        wget https://musl.cc/aarch64-linux-musl-cross.tgz -O musl-cross.tgz; \
    else \
        echo "Unsupported architecture: $ARCH" && exit 1; \
    fi && \
    tar -xzf musl-cross.tgz -C /opt && \
    rm musl-cross.tgz && \
    ln -s /opt/*-linux-musl-cross/bin/*musl-gcc /usr/local/bin/musl-gcc

# Build musl-linked Python from source and install it alongside system Python
RUN wget https://www.python.org/ftp/python/3.12.0/Python-3.12.0.tgz && \
    tar -xzf Python-3.12.0.tgz && \
    cd Python-3.12.0 && \
    CC=musl-gcc ./configure --prefix=/opt/python-musl --disable-shared --enable-static && \
    make -j$(nproc) && \
    make altinstall && \
    cd .. && rm -rf Python-3.12.0 Python-3.12.0.tgz

# Install Nuitka using the musl-linked Python
RUN /opt/python-musl/bin/python3.12 -m ensurepip && \
    /opt/python-musl/bin/pip3.12 install --no-cache-dir nuitka

# --------------------------------------------------------------------------
# VSCode-specific Setup
# --------------------------------------------------------------------------

RUN chsh -s /bin/zsh vscode
USER vscode
RUN sudo chown -R vscode:vscode /workspace

# Default CMD for devcontainer
CMD ["sleep", "infinity"]
