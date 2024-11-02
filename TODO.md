# TODO

- collect corpus, upload tarball to API
- CorpusRevision
  - Basic commands: init and sync with hashes, efficiently

# Next

- why does "Authenticating by encoding client credentials" get called twice?
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
