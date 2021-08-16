from typing import ClassVar

import envtoml
from app.utils import resolve_root

_CONFIG_FILE_PATH = resolve_root('config/app.toml')

class ConfigManager:
    _config_dict: ClassVar[dict]

    @classmethod
    def load_config(cls):        
        with open(_CONFIG_FILE_PATH) as f:
            cls._config_dict = envtoml.load(f)

    @classmethod
    def get(cls, key: str, default=None):
        """
        Returns the value of the config from the given key.

        Supports nested config using the dotted key notation.
        E.g key = 'db.main.user'
        """
        if not key:
            raise KeyError("Invalid key")
        current = cls._config_dict
        for p in key.split('.'):
            try:
                current = current[p]
            except:
                return default
        return current


    @classmethod
    def get_bool(cls, key: str):
        val = cls.get(key)

        # Make sure it also works for env parsers that convert the string 'true' to the value `True`
        return val is True or val == 'true'
