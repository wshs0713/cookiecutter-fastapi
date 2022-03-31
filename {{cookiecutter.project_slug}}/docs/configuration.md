# Configuration

path: `{{cookiecutter.project_slug}}/config/`

## `.env` file

**NOTE**: Due to security issues, the `.env` files are not included in this repository, please set it yourself or get it from the remote server.

### Files

- `.env.dev`: For development environment.
- `.env.test`: For test environment.
- `.env.prod`: For production environment.

### Environment variables

Environment variables description:

- `ENV`: Environment (development, test, production)
- `SECRET_KEY`: Secret key
- `API_PREFIX`: API prefix.
- `CORS_WHITELIST`: CORS whitelist, use `,` as separator.
- `PROJECT_DIR`: Project directory.

## `gunicorn_config.py`

The config file for `Gunicorn`, see also [Gunicorn Settings](https://docs.gunicorn.org/en/stable/settings.html)
