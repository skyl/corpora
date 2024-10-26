#!/bin/bash

# If a command is passed, run it (useful for CI).
if [ $# -gt 0 ]; then
  exec "$@"
else
  # smell
  git config --global --add safe.directory /workspace
  sleep infinity
fi
