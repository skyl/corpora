#!/bin/bash
set -e

rm -rf packages/corpora_client
mkdir -p packages/corpora_client/docs packages/corpora_client/test
rm -rf gen/corpora_client
openapi-generator-cli generate -i http://app:8877/api/openapi.json \
    -g python -o gen/corpora_client \
    --additional-properties=packageName=corpora_client
    # --additional-properties=library=asyncio
    # --additional-properties=generateSourceCodeOnly=true
# TODO: doesn't resolve in the IDE - so ... do something about that.
# pip install -e /workspace/py/gen/corpora_client
# TODO: this is fragile.
cp -r gen/corpora_client/corpora_client/* packages/corpora_client
cp -r gen/corpora_client/docs/* packages/corpora_client/docs
cp -r gen/corpora_client/test/* packages/corpora_client/test
cp gen/corpora_client/README.md packages/corpora_client/README.md
cp gen/corpora_client/setup.py packages/corpora_client/setup.py
cp gen/corpora_client/requirements.txt packages/corpora_client/requirements.txt
cp gen/corpora_client/test-requirements.txt packages/corpora_client/test-requirements.txt
rm -rf gen/corpora_client
black .
pytest
