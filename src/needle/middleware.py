from typing import Callable

from fastapi import Request
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        """
        Middleware to automatically log all requests and responses.

        Args:
            request (Request): The request object.
            call_next (Callable): The next middleware in the chain.

        Returns:
            Response: The response object.

        """
        address_ip = request.client.host
        port = request.client.port

        # if ping to metrics, ignore logging
        if request.url.path == "/metrics":
            return await call_next(request)

        # Log the request
        logger.info(f"{address_ip}:{port} - {request.method} - {request.url}")

        # Call the next middleware
        return await call_next(request)
