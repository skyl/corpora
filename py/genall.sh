rm -rf gen/core_client
openapi-generator-cli generate -i http://127.0.0.1:8000/api/openapi.json \
    -g python -o gen/corpora_client \
    --additional-properties=packageName=corpora_client \
    --additional-properties=library=asyncio
    # --additional-properties=generateSourceCodeOnly=true
black .
pip install -e /workspace/py/gen/corpora_client
