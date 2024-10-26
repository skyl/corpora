#!/bin/bash

# Add Zsh history persistence
echo 'autoload -Uz add-zsh-hook; append_history() { fc -W }; add-zsh-hook precmd append_history; export HISTFILE=/home/vscode/.corpora.zsh_history/.zsh_history' >> ~/.zshrc
touch /home/vscode/.corpora.zsh_history/.zsh_history
