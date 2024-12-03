import logging
import os

import typer
from typer import Typer

from needle import CONFIG_PATH
from needle.settings import Settings

cli = Typer()


@cli.command()
def run(
    app: str = typer.Option("needle.app:app", envvar="APP", help="Application to launch."),
    host: str = typer.Option("localhost", envvar="HOST", help="Address on which the server should listen."),
    port: int = typer.Option(8000, envvar="PORT", help="Port on which the server should listen."),
    workers: int = typer.Option(1, help="Number of worker processes to use."),
    debug: bool = typer.Option(False, envvar="DEBUG", help="Enable debug mode."),
):
    """
    Start the server with the given parameters.

    Args:
        app (str): Application to launch.
        host (str): Host IP address of the server.
        port (int): Port number of host server.

    """
    print(f"Starting the server with host: '{host}' and port: '{port}'")

    # Save the settings for uvicorn child processes
    settings = Settings(debug=debug)
    settings.to_toml(CONFIG_PATH)

    # Run the FastAPI application with the given environment
    launch_app(
        app=app,
        host=host,
        port=port,
        workers=workers,
    )


def launch_app(
    app: str = "needle.app:app",
    host: str = "localhost",
    port: int = 8000,
    workers: int = None,
):
    """
    Launch the FastAPI application with the given parameters.

    Args:
        app (str): Application to launch.
        host (str): Host IP address of the server.
        port (int): Port number of host server.
        workers (int): Number of worker processes to use.

    """
    import uvicorn

    if (workers is None) or (workers < 1):
        workers = max(1, os.cpu_count())

    print(f"Number of workers: {workers} (max: {os.cpu_count()})")

    uvicorn.run(
        app=app,
        host=host,
        port=port,
        workers=workers,
    )
