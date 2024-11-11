# TODO

- `corpora workon README.md`

# Next

- static prompt context + dynamic RAG context
  - .corpora/GOALS.md
  - .corpora/ISSUES.md
  - .corpora/PREFERENCES.md
  ?
- nearest neighbor vector search endpoint(s)
  - compare vector of summary versus vector of splits, create search endpoint(s) test adhoc queries
- more CI checks, local tools - rm unused imports, for instance (on save, in CI..)
- async upload, progress bard ... ?
- publish to pypi
- consider ruff
- pr-agent only on comments?
- add full oauth 3 leg to CLI
  - https://django-oauth-toolkit.readthedocs.io/en/latest/getting_started.html#
- pytest --cov=. --cov-report term
  - more facilities for static analysis, test coverage, complexity checks

- **Start interactive?** Could be cool to just say things to do "rewrite foo/bar/baz.py with BazPlex"
  - agents ... function calling ... maybe we have a menu of function `mkdir`, `create file`, `rewrite file`
    * Take input. Analyze problem. Choose sequence of agents. Let agents execute in order. Report back to user.
