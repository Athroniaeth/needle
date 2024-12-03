from datetime import datetime
from typing import Callable

from fastapi import Request
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
        today = datetime.now()

        # Log the request
        print(f"{today} - {address_ip}:{port} - {request.method} - {request.url}")

        # Call the next middleware
        return await call_next(request)
