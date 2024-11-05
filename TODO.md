# TODO

- compare vector of summary versus vector of splits, create search endpoint(s) test adhoc queries

- test full init with chained tasks

- Python split with AST - langchain one is kinda' lame.

- for small corpora, we could get away with a mega-task but let's break into many single responsibilities
  - finish ingest for real
  - Start building the real records for the `corpora` corpus
    - name should be unique per owner?
    - handle validation errors in the CLI

- logging in celery - logging best practive everywhere.

- CorpusRevision (?), models migration pass
  - Basic commands: init and sync with hashes, efficiently
  - easy to do whole tarballs with small corpus, but we should try on larger soon

- consider include/exclude in corpora.yaml or similar? Right now just use git ls-files...
- default command is init/sync and it's smart to know which
  - normal workflow is just to run `corpora` to init or sync

- **Start interactive?** Could be cool to just say things to do "rewrite foo/bar/baz.py with BazPlex"
  - agents ... function calling ... maybe we have a menu of function `mkdir`, `create file`, `rewrite file`
    * Take input. Analyze problem. Choose sequence of agents. Let agents execute in order. Report back to user.

- more CI checks, local tools - rm unused imports, for instance (on save, in CI..)

# Next

- async upload, progress bard ... ?
- publish to pypi
- consider ruff
- pr-agent only on comments?
- add full oauth 3 leg to CLI
  - https://django-oauth-toolkit.readthedocs.io/en/latest/getting_started.html#

# Done

- Start structure
- LICENSE
- how to install postgres
- devcontainer
- devcontainer history
- GH actions build/test/lint python
  - Same devcontainer works for both? no, maybe later, still early
  - choose python linting tool (black)
- corpora_proj README, all READMEs at all levels
- add pr-agent?
- .devcontainer/README.md
- main branch protection
- Start core models
- Model Files / Splits - how to interface as customer? Internal should be same?
  - (think) CLI, API, is there a way to talk to DB directly? LFG
- Start API
- corpora_client generated
  - prove client works
- auth/auth for API endpoints, Corpus ownership
- CLI that hits API
  - API spec, generation (?)
- `import corpora_client` in editor doesn't resolve
- harden devops
- why does "Authenticating by encoding client credentials" get called twice?
- collect corpus, upload tarball to API
- introduce celery (?) or similar for async tasks
- handle the file (sync/async) upload in the API
- vector length in models versus oai implementation
- langchain-text-splitters - split based on type, cohesive approach, python and md


