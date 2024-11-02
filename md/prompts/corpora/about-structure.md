Corpora is a git repository, a body of software.

https://github.com/skyl/corpora

```txt
.
├── .corpora.yaml
├── .devcontainer
│   ├── Dockerfile
│   ├── README.md
│   ├── devcontainer.json
│   ├── entrypoint.sh
│   └── setup.sh
├── .gitattributes
├── .github
│   └── workflows
│       ├── README.md
│       ├── ci-python.yml
│       ├── pgvector17.yml
│       └── pr-agent.yml
├── .gitignore
├── .pr_agent.toml
├── .vscode
│   └── settings.json
├── CODEOWNERS
├── LICENSE
├── NOTICE
├── README.md
├── TODO.md
├── docker
│   └── Dockerfile.pgvector
├── docker-compose.yaml
├── md
│   ├── README.md
│   ├── SETUP.md
│   └── prompts
│       └── about-corpora.md
└── py
    ├── .gitignore
    ├── README.md
    ├── genall.sh
    ├── openapitools.json
    ├── packages
    │   ├── README.md
    │   ├── corpora
    │   │   ├── README.md
    │   │   ├── __init__.py
    │   │   ├── admin.py
    │   │   ├── api.py
    │   │   ├── apps.py
    │   │   ├── auth.py
    │   │   ├── docs
    │   │   │   └── json_field_metadata.md
    │   │   ├── lib
    │   │   │   ├── README.md
    │   │   │   ├── __init__.py
    │   │   │   ├── dj
    │   │   │   │   ├── __init__.py
    │   │   │   │   ├── decorators.py
    │   │   │   │   └── test_decorators.py
    │   │   │   ├── files.py
    │   │   │   └── test_files.py
    │   │   ├── migrations
    │   │   │   ├── 0001_enable_vector_extension.py
    │   │   │   ├── 0002_initial.py
    │   │   │   ├── 0003_corpus_owner.py
    │   │   │   └── __init__.py
    │   │   ├── models.py
    │   │   ├── requirements.txt
    │   │   ├── schema.py
    │   │   ├── test_api.py
    │   │   └── test_models.py
    │   ├── corpora_cli
    │   │   ├── README.md
    │   │   ├── __init__py
    │   │   ├── auth.py
    │   │   ├── commands
    │   │   │   ├── __init__.py
    │   │   │   ├── corpus.py
    │   │   │   └── file.py
    │   │   ├── config.py
    │   │   ├── main.py
    │   │   ├── requirements.txt
    │   │   ├── test_auth.py
    │   │   └── test_config.py
    │   ├── corpora_client
    │   │   ├── README.md
    │   │   ├── corpora_client
    │   │   │   ├── __init__.py
    │   │   │   ├── api
    │   │   │   │   ├── __init__.py
    │   │   │   │   └── corpora_api.py
    │   │   │   ├── api_client.py
    │   │   │   ├── api_response.py
    │   │   │   ├── configuration.py
    │   │   │   ├── exceptions.py
    │   │   │   ├── models
    │   │   │   │   ├── __init__.py
    │   │   │   │   ├── corpus_response_schema.py
    │   │   │   │   ├── corpus_schema.py
    │   │   │   │   ├── file_response_schema.py
    │   │   │   │   └── file_schema.py
    │   │   │   ├── py.typed
    │   │   │   └── rest.py
    │   │   ├── docs
    │   │   │   ├── CorporaApi.md
    │   │   │   ├── CorpusResponseSchema.md
    │   │   │   ├── CorpusSchema.md
    │   │   │   ├── FileResponseSchema.md
    │   │   │   └── FileSchema.md
    │   │   ├── requirements.txt
    │   │   ├── setup.py
    │   │   └── test-requirements.txt
    │   └── corpora_proj
    │       ├── README.md
    │       ├── __init__.py
    │       ├── asgi.py
    │       ├── manage.py
    │       ├── settings.py
    │       ├── urls.py
    │       └── wsgi.py
    ├── pyproject.toml
    ├── pytest.ini
    ├── requirements-dev.txt
    └── requirements.txt

23 directories, 97 files
```

The purpose of the Corpora project is to build tools that will help build other corpora.

Corpora will soon build itself as it builds tools to build other arbitrary repositories.

What we are working on now:
    - build the perfect scalable polyglot monorepo, focusing on Python first
    - utilize pgvector with Django to sync repositories to postgres+AI (starting with corpora itself)
    - build a beautiful, modern, modular CLI that interacts seamlessly with the API
    - run locally in our devcontainer within corpora repo first but we need to be able to publish in a variety of ways: modules to pypi, containers, gitops to our own k8s, etc.
    - the software must be top-quality, perfectly tested with the latest best tools
