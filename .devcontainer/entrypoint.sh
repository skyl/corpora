#!/bin/bash

# If a command is passed, run it (useful for CI).
if [ $# -gt 0 ]; then
  echo "RUNNING"
  exec "$@"
else
  # smell
  echo "SLEEPING"
  git config --global --add safe.directory /workspace
  sleep infinity
fi
