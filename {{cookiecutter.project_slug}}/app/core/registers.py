"""Application registry."""
import logging.config
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette_exporter import PrometheusMiddleware, handle_metrics
from api.routes import analysis
from middlewares.http import custom_http_middleware
from core.config import APIConfig, get_config
from core.error_handlers import (
    http_exception_handler,
    validation_exception_handler,
    all_exception_handler
)


class FastAPIRegister:
    """FastAPI register."""
    app: FastAPI = None
    config: APIConfig = get_config()

    def __init__(self):
        """FastAPI initialize."""
        self.config = get_config()
        self.app = FastAPI(
            title=self.config.API_NAME,
            version=self.config.API_VERSION,
            redoc_url=None,
            docs_url=f'{self.config.API_PREFIX}/api/docs',
            openapi_url=f'{self.config.API_PREFIX}/api/openapi.json'
        )

        self.create_directory()

        # Logging configuration
        logging.config.dictConfig(self.config.LOG_CONFIG)

        self.register_router()
        self.register_middleware()
        self.register_exception_handler()

    def create_app(self):
        """Create FastAPI.

        Returns:
            FastAPI: FastAPI application.
        """
        return self.app

    def register_router(self):
        """Register routers."""
        self.app.include_router(analysis.router, prefix=f'{self.config.API_PREFIX}/api')
        self.app.add_route(f'{self.config.API_PREFIX}/api/metrics', handle_metrics)

    def register_middleware(self):
        """Register middlewares."""
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=self.config.cors_whitelist,
            allow_credentials=True,
            allow_methods=['GET,POST,OPTIONS'],
            allow_headers=['*']
        )
        self.app.add_middleware(
            PrometheusMiddleware,
            app_name='{{cookiecutter.project_slug}}',
            group_paths=True
        )
        self.app.add_middleware(
            BaseHTTPMiddleware,
            dispatch=custom_http_middleware
        )

    def register_exception_handler(self):
        """Register exception handler."""
        self.app.add_exception_handler(HTTPException, http_exception_handler)
        self.app.add_exception_handler(StarletteHTTPException, http_exception_handler)
        self.app.add_exception_handler(RequestValidationError, validation_exception_handler)
        self.app.add_exception_handler(Exception, all_exception_handler)

    def create_directory(self):
        """Create the required directories."""
        directory = [
            self.config.LOG_DIR
        ]

        for item in directory:
            item.mkdir(parents=True, exist_ok=True)
