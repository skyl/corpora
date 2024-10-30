#!/bin/bash
set -e

rm -rf gen/corpora_client
openapi-generator-cli generate -i http://127.0.0.1:8000/api/openapi.json \
    -g python -o gen/corpora_client \
    --additional-properties=packageName=corpora_client
    # --additional-properties=library=asyncio
    # --additional-properties=generateSourceCodeOnly=true
black .
# TODO: doesn't resolve in the IDE - so ... do something about that.
pip install -e /workspace/py/gen/corpora_client
