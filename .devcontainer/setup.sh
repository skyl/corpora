#!/bin/bash

# random stuff ... hrm ...
# echo "starting zsh..."
echo 'autoload -Uz add-zsh-hook; append_history() { fc -W }; add-zsh-hook precmd append_history; export HISTFILE=/home/vscode/.corpora.zsh_history/.zsh_history' >> ~/.zshrc
echo alias tree="tree -I '.venv|node_modules|__pycache__|.git|.pytest_cache' -a" >> ~/.zshrc
# TODO: corpora_client dev experience has to be 100
pip install -e /workspace/py/gen/corpora_client
zsh
