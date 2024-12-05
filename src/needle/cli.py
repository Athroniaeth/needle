import os

import typer
from loguru import logger
from typer import Typer

from needle import CONFIG_PATH
from needle._logging import setup_logger, Level
from needle.settings import Settings

cli = Typer()


@cli.command()
def run(
    app: str = typer.Option("needle.app:app", envvar="APP", help="Application to launch."),
    host: str = typer.Option("localhost", envvar="HOST", help="Address on which the server should listen."),
    port: int = typer.Option(8000, envvar="PORT", help="Port on which the server should listen."),
    workers: int = typer.Option(1, help="Number of worker processes to use."),
    debug: bool = typer.Option(False, envvar="DEBUG", help="Enable debug mode."),
    log_level: Level = typer.Option(Level.INFO, envvar="LOG_LEVEL", help="Logging level for the application."),
):
    """
    Start the server with the given parameters.

    Args:
        app (str): Application to launch.
        host (str): Host IP address of the server.
        port (int): Port number of host server.
        workers (int): Number of worker processes to use.
        debug (bool): Enable debug mode.
        log_level (Level): Logging level for the application.

    """
    # Setup the logger for the application
    setup_logger(level=log_level)

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

    # Log the start of the server
    logger.info(f"Starting the server with host: '{host}' and port: '{port}'")

    # Get the number of workers to use
    max_workers = os.cpu_count()
    workers = 1 if workers is None else workers
    workers = max_workers if workers < 1 else workers
    workers = min(workers, max_workers)

    logger.info(f"Uvicorn start server with {workers}/{max_workers} workers")

    uvicorn.run(
        app=app,
        host=host,
        port=port,
        workers=workers,
    )
