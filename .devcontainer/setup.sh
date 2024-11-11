#!/bin/bash

echo 'autoload -Uz add-zsh-hook; append_history() { fc -W }; add-zsh-hook precmd append_history; export HISTFILE=/home/vscode/.corpora.zsh_history/.zsh_history' >> ~/.zshrc
echo "alias tree=\"tree -I '\\.venv|node_modules|__pycache__|\\.git|\\.pytest_cache' -a\"" >> ~/.zshrc
sudo ln -s /workspace/py/packages/corpora_cli/main.py /usr/local/bin/corpora
