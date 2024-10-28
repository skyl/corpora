FROM mcr.microsoft.com/devcontainers/python:3.12

# Install PostgreSQL client, zsh, wget, and OpenJDK, and download OpenAPI Generator
RUN apt-get update && \
    apt-get install -y postgresql-client zsh wget openjdk-11-jre && \
    rm -rf /var/lib/apt/lists/* && \
    wget https://repo1.maven.org/maven2/org/openapitools/openapi-generator-cli/6.6.0/openapi-generator-cli-6.6.0.jar -O /usr/local/bin/openapi-generator-cli.jar && \
    echo 'alias openapi-generator="java -jar /usr/local/bin/openapi-generator-cli.jar"' >> /root/.bashrc

# Set up the workspace and install Python dependencies
WORKDIR /workspace
COPY py/requirements.txt /workspace/requirements.txt
COPY py/requirements-dev.txt /workspace/requirements-dev.txt
COPY py/packages/corpora/requirements.txt /workspace/packages/corpora/requirements.txt
RUN pip install --no-cache-dir -r /workspace/requirements.txt

# Set zsh as the default shell for the vscode user
RUN chsh -s /bin/zsh vscode

# Keep container running with sleep (ideal for devcontainers)
CMD ["sleep", "infinity"]
