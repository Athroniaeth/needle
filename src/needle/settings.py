from enum import StrEnum
from typing import Any, Type

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(StrEnum):
    """
    Environment to use (local or ovh cloud).

    Notes:
        - DEVELOPMENT: Local environment (without Docker, without SSL).
        - PRODUCTION: Production environment (with Docker, with SSL).

    """

    DEVELOPMENT = "development"
    PRODUCTION = "production"
    STAGING = "staging"


class Settings(BaseSettings):
    """
    Configuration settings for the entire application.

    Attributes:
        environment (Environment): Environment to use
        host (str): Server host IP address.
        model_config (SettingsConfigDict): Model configuration.

    """

    # Environment configuration CLI
    domain: str = Field("localhost", alias="DOMAIN")

    # Network server configuration
    host: str = Field(default="localhost", alias="HOST")
    port: int = Field(default=8000, alias="PORT")

    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def uri(self) -> str:
        """
        Get the URI with the given environment variables.

        Returns:
            str: The URI with the given environment variables.

        """
        return f"https://{self.domain}" if "localhost" not in self.domain else f"http://{self.domain}"

    @property
    def uri_callback(self) -> str:
        """
        Get the URI with the given environment variables.

        Returns:
            str: The URI with the given environment variables.

        """
        return f"{self.uri}/callback"


class DevelopmentSettings(Settings):
    """
    Settings for the development environment.

    Notes:
        - Force host to 'localhost"
        - Force port to 7860
        - Force domain with port

    """

    def model_post_init(self, __context: Any):  # noqa: D102
        self.host = "localhost"
        self.port = 8000

        self.domain = f"{self.host}:{self.port}"


class StagingSettings(Settings):
    """
    Settings for the staging environment.

    Notes:
        - Force host to '0.0.0.0'
        - Force port to 8000

    """

    def model_post_init(self, __context: Any):  # noqa: D102
        self.host = "0.0.0.0"  # noqa: S104
        self.port = 8000
        self.domain = f"http://{self.domain}"


class ProductionSettings(Settings):
    """
    Settings for the production environment.

    Notes:
        - Force host to '0.0.0.0'
        - Force port to 8000 (Nginx handle SSL)
        - Force domain without port (Nginx handle port 443)

    """

    def model_post_init(self, __context: Any):  # noqa: D102
        self.host = "0.0.0.0"  # noqa: S104
        self.port = 8000
        self.domain = f"https://{self.domain}"


def get_info_environment(environment: Environment = Environment.DEVELOPMENT) -> Type[Settings]:
    """
    Get the information of the environment.

    Args:
        environment (Environment): The environment to use.

    Returns:
        Type[Settings]: The settings class of the environment.

    """
    mapping = {
        Environment.DEVELOPMENT: DevelopmentSettings,
        Environment.PRODUCTION: ProductionSettings,
        Environment.STAGING: StagingSettings,
    }

    result = mapping.get(environment)

    if result is None:
        raise ValueError(f"Invalid environment: {environment}")

    return result
