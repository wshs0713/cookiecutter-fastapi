"""Main application."""
import logging.config
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette_exporter import PrometheusMiddleware, handle_metrics
from .middlewares.http import custom_http_middleware
from .core.config import APIConfig, get_config
from .core.error_handlers import (
    http_exception_handler, validation_exception_handler, all_exception_handler
)


def create_app() -> FastAPI:
    """Create FastAPI.

    Returns:
        FastAPI: FastAPI application.
    """
    config = get_config()

    app = FastAPI(
        title=config.API_NAME,
        version=config.API_VERSION,
        redoc_url=None,
        docs_url='/api/docs',
        openapi_url='/api/openapi.json'
    )

    create_directory(config)

    # Logging configuration
    logging.config.dictConfig(config.LOG_CONFIG)

    register_router(app, config)
    register_middleware(app, config)
    register_exception_handler(app)

    return app


def register_router(app: FastAPI, config: APIConfig):
    """Register routers.

    Args:
        app (FastAPI): FastAPI.
        config (APIConfig): API configuration.
    """
    app.add_route('/api/metrics', handle_metrics)


def register_middleware(app: FastAPI, config: APIConfig):
    """Register middlewares.

    Args:
        app (FastAPI): FastAPI.
        config (APIConfig): API configuration.
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.cors_whitelist,
        allow_credentials=True,
        allow_methods=['GET,POST,OPTIONS'],
        allow_headers=['*']
    )
    app.add_middleware(
        PrometheusMiddleware,
        app_name='{{cookiecutter.project_slug}}',
        group_paths=True
    )
    app.add_middleware(
        BaseHTTPMiddleware,
        dispatch=custom_http_middleware
    )


def register_exception_handler(app: FastAPI):
    """Register exception handler.

    Args:
        app (FastAPI): FastAPI.
    """
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, all_exception_handler)


def create_directory(config: APIConfig):
    """Create the required directories.

    Args:
        config (APIConfig): API configuration.
    """
    directory = [
        config.LOG_DIR
    ]

    for item in directory:
        item.mkdir(parents=True, exist_ok=True)
