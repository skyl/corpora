#!/bin/bash

# random stuff ... hrm ...
# echo "starting zsh..."
echo 'autoload -Uz add-zsh-hook; append_history() { fc -W }; add-zsh-hook precmd append_history; export HISTFILE=/home/vscode/.corpora.zsh_history/.zsh_history' >> ~/.zshrc
echo alias tree="tree -I '.venv|node_modules|__pycache__|.git|.pytest_cache' -a" >> ~/.zshrc
pip install -e /workspace/py/gen/corpora_client
zsh
