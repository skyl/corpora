# Notes on environment setup

You can clone the repo and install things on your host. This will be left up to you. Better, use the devcontainer with VSCode.

## Python

To work on the python without devcontainer, you can use Python 3.12 in the root.

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r py/requirements.txt
```

## Postgres

### MacOS

<!-- Wait, shouldn't we just have a devcontainer? -->

See [../.devcontainer/devcontainer.json](../.devcontainer/devcontainer.json).
