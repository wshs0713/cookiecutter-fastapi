"""HTTP middleware."""
import time
import logging
from fastapi import Request


async def custom_http_middleware(request: Request, call_next):
    """Custom HTTP middleware to log execution time.

    Args:
        request (Request): FastAPI Request.
        call_next: FastAPI call_next.

    Returns:
        call_next: FastAPI call_next.
    """
    start_time = time.time()
    response = await call_next(request)
    exec_time = f'{(time.time() - start_time):.6f}s'

    ip = request.headers.get('X-Forwarded-For', request.client.host)
    user_agent = request.headers.get('User-Agent')
    scheme = f'{request.url.scheme.upper()}/{request.scope.get("http_version")}'

    logger = logging.getLogger(__name__)
    logger.info(f'''
        {ip} - "{request.method} {request.url.path} {scheme}" {response.status_code} {exec_time}
        "{user_agent}"
    ''')

    return response
