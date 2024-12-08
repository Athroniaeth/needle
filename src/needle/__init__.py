from pathlib import Path

from needle.settings import Settings

# Define the global paths for the project
PROJECT_PATH = Path(__file__).parents[2].absolute()
SRC_PATH = PROJECT_PATH / "src"
APP_PATH = SRC_PATH / "needle"

# Define the path to the environment file
ENV_PATH = PROJECT_PATH / ".env"
STATIC_PATH = APP_PATH / "static"
LOGGING_PATH = PROJECT_PATH / ".log"
CONFIG_PATH = PROJECT_PATH / "config.toml"
TEMPLATE_PATH = APP_PATH / "templates"

# Global settings for the application
settings = Settings(_env_file=ENV_PATH)
