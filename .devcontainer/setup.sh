#!/bin/bash

# zsh history
echo 'autoload -Uz add-zsh-hook; append_history() { fc -W }; add-zsh-hook precmd append_history; export HISTFILE=/home/vscode/.corpora.zsh_history/.zsh_history' >> ~/.zshrc
# Aliases
echo "alias tree=\"tree -I '\\.venv|node_modules|build|target|dist|test-corpora|__pycache__|\\.git|\\.pytest_cache' -a\"" >> ~/.zshrc
echo "alias git-delete-branches=\"git branch | grep -v 'main' | xargs git branch -d\"" >> ~/.zshrc
# Alias for dumpdir
echo 'alias dumpdir=\"git ls-files | xargs file --mime-type | grep 'text/' | cut -d: -f1 | while read -r file; do echo -e \\\"\\n==== Contents of: \$file ====\\n\\\"; cat \\\"\$file\\\"; done\"' >> ~/.zshrc
# Symbolic link for corpora
sudo ln -s /workspace/py/packages/corpora_cli/main.py /usr/local/bin/corpora
# Rust on PATH
echo "export PATH=\"/home/vscode/.cargo/bin:\${PATH}\"" >> ~/.zshrc
