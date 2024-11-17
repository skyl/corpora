# TODO

- build rust CLI to try across platforms in different corpora, evaluate rust for CLI
  - https://rust-cli.github.io/book/index.html
  - Corpus!!

# Next

- label issue
- more python CI checks, local tools - rm unused imports, for instance (on save, in CI..)
  - consider ruff - one shot to rule them all
  - pytest --cov=. --cov-report term
    - more facilities for static analysis, test coverage, complexity checks
  - publish to pypi
  - publish containers
  - pr-agent only on comments?
- async upload, progress bar ... ?
  - rust or python? ;9
- add full oauth 3 leg to CLI
  - https://django-oauth-toolkit.readthedocs.io/en/latest/getting_started.html#
  - rust or python ;/

- **Start interactive?** Could be cool to just say things to do "rewrite foo/bar/baz.py with BazPlex"
  - agents ... function calling ... maybe we have a menu of function `mkdir`, `create file`, `rewrite file`
    * Take input. Analyze problem. Choose sequence of agents. Let agents execute in order. Report back to user.
  - rust?


# Done

- `corpora workon README.md`
- static prompt context + dynamic RAG context
  - .corpora/GOALS.md
  - .corpora/ISSUES.md
  - .corpora/PREFERENCES.md
  ?
- nearest neighbor vector search endpoint(s)
  - compare vector of summary versus vector of splits, create search endpoint(s) test adhoc queries
- `corpora plan update_issue 17`
