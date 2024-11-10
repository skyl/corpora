# TODO

- Abstract PM (issues) interface
  - GH implementation
  - killer feature: "make issue" in CLI with RAG corpora context
    - static prompt context + dynamic RAG context
      - .corpora/GOALS.md
      - .corpora/ISSUES.md
      - .corpora/PREFERENCES.md
      ?

- namespace `tasks.py` into directory
  - test tasks

- nearest neighbor vector search endpoint(s)
  - compare vector of summary versus vector of splits, create search endpoint(s) test adhoc queries

- [CORPUS] Sync versus init
  - CorpusRevision (?), models migration pass
    - Basic commands: init and sync with hashes, efficiently
    - easy to do whole tarballs with small corpus, but we should try on larger soon
  - default command is init/sync and it's smart to know which
    - normal workflow is just to run `corpora` to init or sync
  - consider include/exclude in corpora.yaml or similar? Right now just use git ls-files...

- Python split with AST - langchain one is kinda' lame.

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
- pytest --cov=. --cov-report term
  - more facilities for static analysis, test coverage, complexity checks
