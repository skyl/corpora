#!/bin/bash

if [ "$CI" = "true" ]; then
  echo "CI mode: not starting interactive shell."
  # exit 0  # Do nothing in CI
  exec "$@"
else
  # Local dev: Drop into Zsh
  echo "Starting Zsh for local development"
  git config --global --add safe.directory /workspace
  # exec zsh
  sleep infinity
fi
