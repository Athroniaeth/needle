import logging

from fastapi import Request, HTTPException
from starlette.responses import JSONResponse


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:  # noqa: F841
    """
    Handle HTTP exceptions and return JSON responses.

    Args:
        request (Request): The request that caused the exception.
        exc (HTTPException): The exception that was raised.

    Returns:
        JSONResponse: A JSON response containing the error details.

    """
    logging.error(f"HTTPException: {exc.detail}")

    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )
