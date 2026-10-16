import logging
import sys
import time
import uuid
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

# Configure logger
logger = logging.getLogger("healix")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(
    '{"time": "%(asctime)s", "level": "%(levelname)s", "name": "%(name)s", "message": "%(message)s"}'
)
handler.setFormatter(formatter)
if not logger.handlers:
    logger.addHandler(handler)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        start_time = time.time()

        # Sanitize path: don't log query parameters that could contain sensitive health queries
        clean_path = request.url.path

        try:
            response = await call_next(request)
            process_time_ms = round((time.time() - start_time) * 1000, 2)

            # Structured audit log omitting request body / headers / auth tokens
            logger.info(
                f'{{"request_id": "{request_id}", "method": "{request.method}", "endpoint": "{clean_path}", '
                f'"status_code": {response.status_code}, "duration_ms": {process_time_ms}}}'
            )
            response.headers["X-Request-ID"] = request_id
            return response
        except Exception as e:
            process_time_ms = round((time.time() - start_time) * 1000, 2)
            logger.error(
                f'{{"request_id": "{request_id}", "method": "{request.method}", "endpoint": "{clean_path}", '
                f'"error": "{type(e).__name__}", "duration_ms": {process_time_ms}}}'
            )
            raise e
