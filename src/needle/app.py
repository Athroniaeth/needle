import gradio as gr
from fastapi import FastAPI, HTTPException
from prometheus_fastapi_instrumentator import Instrumentator

from needle import CONFIG_PATH
from needle.exception import http_exception_handler
from needle.interface import get_gradio_app
from needle.middleware import LoggingMiddleware
from needle.config import Config


def get_fastapi_app(
    debug: bool = True,
):
    """
    Create a FastAPI application with the necessary configurations.

    Returns:
        FastAPI: FastAPI application instance.

    """
    app = FastAPI(debug=debug)

    # Middleware
    app.add_middleware(LoggingMiddleware)

    # Exceptions handlers
    app.add_exception_handler(HTTPException, http_exception_handler)

    # Initialize and configure the Prometheus instrument
    Instrumentator().instrument(app).expose(app)

    @app.get(path="/hello")
    def hello():
        return {"hello": "world"}

    return app


# Check if the script is run by uvicorn

# Get config create by CLI
settings = Config.from_toml(CONFIG_PATH)

"""
WARNING: Don't use '/' for path, gradio prevents prometheus
from retrieving information as gradio modifies routes.
Routes defined as /metrics are hidden by the Gradio application mounted on '/'.
"""
# Get the FastAPI application
app = get_fastapi_app(debug=settings.debug)

# Get the Gradio application
blocks = get_gradio_app(
    model_name=settings.model_name,
    prompt_template=settings.prompt_template,
)

# Mount the Gradio application
app = gr.mount_gradio_app(
    app=app,
    path="/app",
    blocks=blocks,
    show_error=settings.debug,
)

from needle import settings

print(f"Settings 3 : {settings}")
