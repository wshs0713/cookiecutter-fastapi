"""Error handlers."""
import logging
from fastapi import Request, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


logger = logging.getLogger('gunicorn.error')


async def http_exception_handler(request: Request, exc: HTTPException):
    """HTTP exception handler.

    Args:
        request (Request): FastAPI Request.
        exc (HTTPException): FastAPI HTTPException.

    Returns:
        JSONResponse: FastAPI JSONResponse.
    """
    logger.error(exc.detail)

    headers = getattr(exc, 'headers', None)
    response = {
        'status': 'failure',
        'error': {
            'status_code': exc.status_code,
            'message': exc.detail
        }
    }

    if headers:
        return JSONResponse(
            status_code=exc.status_code,
            content=response,
            headers=headers
        )

    return JSONResponse(
        status_code=exc.status_code,
        content=response
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Validation exception handler.

    Args:
        request (Request): FastAPI Request.
        exc (RequestValidationError): FastAPI RequestValidationError.

    Returns:
        JSONResponse: FastAPI JSONResponse.
    """
    location = ', '.join(exc.errors()[0]['loc'])
    error_message = f'Location: {location}; msg: {exc.errors()[0]["msg"]}'
    logger.error(error_message)

    response = {
        'status': 'failure',
        'error': {
            'status_code': status.HTTP_400_BAD_REQUEST,
            'message': error_message
        }
    }

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=response
    )


async def all_exception_handler(request: Request, exc: Exception):
    """All exception handler.

    Args:
        request (Request): FastAPI Request.
        exc (Exception): FastAPI Exception.

    Returns:
        JSONResponse: FastAPI JSONResponse.
    """
    ip = request.headers.get('X-Forwarded-For', request.client.host)
    user_agent = request.headers.get('User-Agent')
    scheme = f'{request.url.scheme.upper()}/{request.scope.get("http_version")}'
    error_message = exc.args[0] if len(exc.args) > 0 else 'Internal server error'

    logger.error(error_message)
    logger.info(f'{ip} - "{request.method} {request.url.path} {scheme}" 500 "{user_agent}"')

    response = {
        'status': 'failure',
        'error': {
            'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'message': error_message
        }
    }

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=response
    )
