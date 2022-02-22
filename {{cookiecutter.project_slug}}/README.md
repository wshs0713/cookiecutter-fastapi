# {{cookiecutter.project_name}}

{{cookiecutter.project_short_description}}  

Table of contents:

- [{{cookiecutter.project_name}}](#cookiecutterproject_name)
  - [Features](#features)
  - [Requirements](#requirements)
  - [Configuration](#configuration)
  - [Installation](#installation)
    - [Installation for development](#installation-for-development)
    - [Installation for production](#installation-for-production)
  - [Project structure](#project-structure)
  - [API document](#api-document)
  - [Changelog](#changelog)

## Features

Describe API features.

## Requirements

- OS: Ubuntu 20.04 x86_64 (It might also work on 16.04 and 18.04)
- Python >= 3.8
- See also [requirements.txt](/requirements/requirements.txt)

## Configuration

Please refer to [Configuration](/docs/configuration.md).

**NOTE**: Due to security issues, the `.env` files are not included in this repository, please set it yourself or get it from the remote server.

## Installation

### Installation for development

Install packages:

```bash
$ make install
```

Start server:

```bash
$ pipenv shell
$ uvicorn asgi:app
```

### Installation for production

Install:

- [Docker](https://docs.docker.com/engine/install/ubuntu/)
- [docker-compose](https://docs.docker.com/compose/install/)

Modify `ports`, `build path`, `volume path` configuration in `docker-compose.yml`, and use the following command to build image and start service:

```bash
# USER_ID: User ID
# GID: Group ID
# VERSION: Docker image version tags

$ make deploy USER_ID=$(id -u) GID=$(id -g) VERSION=<version>
```

**NOTE**:

- We use `Uvicorn` and `Gunicorn` for production:
  - `Uvicorn`: A lightning-fast "ASGI" server. It runs asynchronous Python web code in a single process.
  - `Gunicorn`: A Python WSGI HTTP Server for **UNIX**. We use `Gunicorn` to manage `Uvicorn` and run multiple concurrent processes.
- Make sure the permission of volume paths are correct.

## Project structure

```text
{{cookiecutter.project_slug}}
    ├─ .github                  # Github Action workflow
    |   └─ workflows
    |       └─ main.yml
    ├─ app/                     # FastAPI application
    |   ├─ api/
    |   |   └─ routes/          # API routes
    |   ├─ core/                # API configuration, error handlers
    |   |   ├─ config.py
    |   |   └─ error_handler.py
    |   ├─ middlewares/         # API middlewares
    |   |   └─ http.py          # HTTP middleware
    |   ├─ models/              # SQLAlchemy models
    |   ├─ schemas/             # Pydantic schemas
    |   ├─ services/            # Business logic
    |   └─ utils/               # Utilities
    ├─ config/:                 # Config files, environment files
    |   ├─ .env.dev             # Environment file for development
    |   ├─ .env.test            # Environment file for test
    |   ├─ .env.prod            # Environment file for production
    |   ├─ example.env          # Environment file example
    |   └─ gunicorn_config.py   # Gunicorn config file, see also https://docs.gunicorn.org/en/stable/settings.html
    ├─ docs/                    # Documents
    |   ├─ CHANGELOG.md
    |   └─ configuration.md
    ├─ logs/                    # Log files
    ├─ prometheus/              # Prometheus data
    ├─ scripts/                 # Shell scripts
    ├─ tests/                   # Tests, following https://github.com/DeepWaveInc/Project_Guideline#testing
    ├─ asgi.py                  # Entry file
    ├─ docker-compose.yml
    ├─ Dockerfile
    ├─ Makefile
    ├─ Pipfile                  # Pipfile for virtual environment
    ├─ README.md
    └─ tox.ini                  # Includes pytest, pytest-cov, flake8...etc. configs.
```

## API document

Please refer to: `<API_URL>/api/docs`.

## Changelog

Please refer to [CHANGELOG](/docs/CHANGELOG.md)
