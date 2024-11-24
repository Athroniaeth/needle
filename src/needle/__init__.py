from pathlib import Path

# Define the global paths for the project
PROJECT_PATH = Path(__file__).parents[2].absolute()
SOURCE_PATH = Path(__file__).parents[1].absolute()
APP_PATH = Path(__file__).parents[0].absolute()

# Define the path to the environment file
ENV_PATH = PROJECT_PATH / ".env"
