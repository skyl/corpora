#!/bin/bash

# Install Python requirements
pip install -r py/requirements.txt

# Add Zsh history persistence
echo 'autoload -Uz add-zsh-hook; append_history() { fc -W }; add-zsh-hook precmd append_history; export HISTFILE=/home/vscode/.zsh_history' >> ~/.zshrc

touch /home/vscode/.zsh_history
