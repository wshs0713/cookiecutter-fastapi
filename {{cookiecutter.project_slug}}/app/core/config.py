"""API configuration."""
import os
from os.path import dirname, join, abspath
from pathlib import Path
from functools import lru_cache
from typing import List
from pydantic import BaseSettings, Field


class APIConfig(BaseSettings):
    """General API configurations."""
    API_NAME = '{{cookiecutter.project_slug}}'
    API_VERSION = Field('1.0.0', env='API_VERSION')

    ENV: str = Field(..., env='ENV')
    SECRET_KEY: str = Field(..., env='SECRET_KEY')
    DEBUG = True
    TESTING = False

    CORS_WHITELIST: str = Field(..., env='CORS_WHITELIST')

    PROJECT_DIR: Path = dirname(dirname(dirname(abspath(__file__))))
    LOG_DIR: Path = join(PROJECT_DIR, 'logs')
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

    LOG_CONFIG = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'class': 'logging.Formatter',
                'format': '%(asctime)s [%(process)s] [%(name)s] [%(levelname)s]: %(message)s',
                'datefmt': '[%Y-%m-%d %H:%M:%S %z]'
            }
        },
        'handlers': {
            'default': {
                'formatter': 'default',
                'class': 'logging.StreamHandler',
                'level': LOG_LEVEL,
                'stream': 'ext://sys.stdout'
            },
            'file': {
                'formatter': 'default',
                'class': 'logging.FileHandler',
                'filename': join(LOG_DIR, 'api.log')
            }
        },
        'root': {
            'handlers': ['default', 'file'],
            'level': LOG_LEVEL
        },
        'loggers': {
            'gunicorn': {'propagate': True},
            'gunicorn.access': {
                'handlers': ['default', 'file'],
                'propagate': True
            },
            'gunicorn.error': {'propagate': True},
            'uvicorn': {'propagate': True},
            'uvicorn.access': {'propagate': False},
            'uvicorn.error': {'propagate': True}
        }
    }

    class Config:
        """Development config."""
        env_file = 'config/.env.dev'
        env_file_encoding = 'utf-8'
        case_sensitive = True

    @property
    def cors_whitelist(self) -> List[str]:
        """CORS whitelist.

        Returns:
            List[str]: CORS whitelist
        """
        return [x.strip() for x in self.CORS_WHITELIST.split(',') if x]


class TestConfig(APIConfig):
    """Test config."""
    DEBUG = False
    TESTING = True

    class Config:
        """Test config."""
        env_file = 'config/.env.test'
        env_file_encoding = 'utf-8'
        case_sensitive = True


class ProdConfig(APIConfig):
    """Production config."""
    DEBUG = False
    TESTING = False

    class Config:
        """Production config."""
        env_file = 'config/.env.prod'
        env_file_encoding = 'utf-8'
        case_sensitive = True


@lru_cache
def get_config() -> APIConfig:
    """Get configuration.

    Returns:
        APIConfig: API config.
    """
    env = os.getenv('ENV', 'development')

    if env == 'test':
        return TestConfig()
    elif env == 'production':
        return ProdConfig()

    return APIConfig()
