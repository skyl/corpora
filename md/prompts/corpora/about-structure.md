Corpora is a git repository, a body of software.

https://github.com/skyl/corpora

```txt
$ tree . -L 5 -da
.
├── .devcontainer
├── .github
│   └── workflows
├── .vscode
├── docker
├── md
│   ├── notes
│   └── prompts
│       └── corpora
├── py
│   └── packages
│       ├── corpora
│       │   ├── docs
│       │   ├── lib
│       │   │   └── dj
│       │   └── migrations
│       ├── corpora_cli
│       │   ├── commands
│       │   └── utils
│       ├── corpora_client
│       │   ├── api
│       │   ├── docs
│       │   ├── models
│       │   └── test
│       └── corpora_proj
└── sh

27 directories
```

The purpose of the Corpora project is to build tools that will help build other corpora.

Corpora will soon build itself as it builds tools to build other arbitrary repositories.

What we are working on now:
    - build the perfect scalable polyglot monorepo, focusing on Python first
    - utilize pgvector with Django to sync repositories to postgres+AI (starting with corpora itself)
    - build a beautiful, modern, modular CLI that interacts seamlessly with the API
    - run locally in our devcontainer within corpora repo first but we need to be able to publish in a variety of ways: modules to pypi, containers, gitops to our own k8s, etc.
    - the software must be top-quality, perfectly tested with the latest best tools
