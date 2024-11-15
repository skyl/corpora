#!/bin/bash

# zsh history
echo 'autoload -Uz add-zsh-hook; append_history() { fc -W }; add-zsh-hook precmd append_history; export HISTFILE=/home/vscode/.corpora.zsh_history/.zsh_history' >> ~/.zshrc
# Aliases
echo "alias tree=\"tree -I '\\.venv|node_modules|build|target|dist|test-corpora|__pycache__|\\.git|\\.pytest_cache' -a\"" >> ~/.zshrc
echo "alias git-delete-branches=\"git branch | grep -v 'main' | xargs git branch -d\"" >> ~/.zshrc
sudo ln -s /workspace/py/packages/corpora_cli/main.py /usr/local/bin/corpora
# Rust on PATH
echo "export PATH=\"/home/vscode/.cargo/bin:\${PATH}\"" >> ~/.zshrc
