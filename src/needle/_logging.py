import logging
from enum import StrEnum
from functools import lru_cache

from loguru import logger

from needle import LOGGING_PATH

DEFAULT_FORMAT = (
    "<blue>{time:YYYY-MM-DD HH:mm:ss}</blue> | "
    "<level>{level}</level> | <red>"
    "<cyan>{extra[short_name]}</cyan>."
    "<cyan>{file}</cyan>:"
    "<cyan>{function}</cyan>:"
    "</red><cyan>{line}</cyan> - "
    "<level>{message}</level>"
)


class Level(StrEnum):
    """Log levels for the application."""

    TRACE = "TRACE"
    DEBUG = "DEBUG"
    INFO = "INFO"
    SUCCESS = "SUCCESS"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
    EXCEPTION = "EXCEPTION"

    def to_loguru(self) -> int:
        """Convert the level to loguru's level."""
        loguru_level = logger._core.levels.get(self.value)  # noqa: Unresolved attribute reference

        if loguru_level is None:
            raise ValueError(f"Loguru level does not exist: '{self.value}'")

        return loguru_level


def custom_filter(record):
    """Custom filter for loguru, allow to transform module name to logger name."""
    record["extra"]["short_name"] = record["name"].split(".")[0]
    return True


def set_level(level: Level):
    """Set the logging level for all handlers."""
    loguru_level = level.to_loguru()

    for index, handler in logger._core.handlers.items():  # noqa
        logger._core.handlers[index]._levelno = loguru_level.no  # noqa

    # Increase the log level to display it even in production
    logger.success(f"Application change the logging level to '{level}'")


def set_level_logging(custom_logger: logging.Logger, logging_level_loguru: Level):
    """Change the logging level of a custom logger."""
    # This loguru_level don't have a corresponding logging_level
    switcher = {
        Level.TRACE: Level.DEBUG,
        Level.SUCCESS: Level.INFO,
        Level.EXCEPTION: Level.CRITICAL,
    }

    logging_level_loguru = switcher.get(logging_level_loguru, logging_level_loguru)

    # Found the corresponding logging level
    logging_level = logging.getLevelName(logging_level_loguru)

    # Intercept stdout of the library with the corresponding level
    custom_logger.setLevel(logging_level)


@lru_cache(maxsize=1)
def setup_logger(
    name: str = "app",
    rotation: str = "06:00",
    retention: str = "30 days",
    level: Level = Level.DEBUG,
    format_: str = DEFAULT_FORMAT,
):
    """
    Setup the logger for the application.

    Args:
        name (str): The name of the logger.
        rotation (str): The rotation time for the logging file.
        retention (str): The retention time for the logging file.
        level (Level): The logging level for the application.
        format_ (str): The format of the logging message.

    """
    log_file = LOGGING_PATH / f"{name}.log"

    # Remove default loguru's handler
    logger.remove(0)

    # Add a new handler for file (will be use for stdout)
    logger.add(
        log_file,
        rotation=rotation,
        retention=retention,
        compression="xz",
        format=format_,
        level=level,
        filter=custom_filter,
    )

    # Change the level of the logger (else not working)
    set_level(level)

    logger.info(f"Logger setup with level: '{level}'")
