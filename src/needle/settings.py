import os
from dataclasses import dataclass
from pathlib import Path
from typing import Union

import toml


@dataclass
class Settings:
    debug: bool = False

    @classmethod
    def from_toml(cls, path: Union[str, os.PathLike]):
        """
        Load the settings from a TOML file.

        Args:
            path (str): Path to the TOML file.

        Returns:
            Settings: Settings instance.

        """
        path = Path(path)

        if not path.exists():
            raise FileNotFoundError(f"Settings file not found at: '{path}'")

        with open(path, "r") as f:
            return cls(**toml.load(f))

    def to_toml(self, path: Union[str, os.PathLike]):
        """
        Save the settings to a TOML file.

        Args:
            path (str): Path to the TOML file.

        """
        path = Path(path)

        if not path.exists():
            path.touch()

        with open(path, "w") as f:
            toml.dump(self.__dict__, f)
