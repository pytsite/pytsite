"""Description.
"""
import yaml as _yaml
from os import path as _path
from abc import ABC as _ABC, abstractmethod as _abstractmethod
from pytsite import util as _util

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Abstract(_ABC):
    """Abstract registry driver.
    """
    _storage = {}

    @_abstractmethod
    def put(self, key: str, value):
        """Set value of the registry.
        """
        pass

    @_abstractmethod
    def get(self, key: str, default):
        """Get value from the registry.
        """
        pass

    @_abstractmethod
    def merge(self, other: dict):
        """Merge other dictionary onto the registry storage.
        """
        pass

    def get_all(self) -> dict:
        """Get all registry's content.
        """
        return self._storage


class Memory(Abstract):
    def put(self, key: str, value):
        """Set value of the registry.
        """
        current = self._storage
        parts = key.split('.')
        i = 1
        l = len(parts)
        for k in parts:
            if i < l:
                if k not in current:
                    current[k] = dict()
                    current = current[k]
                elif k in current and isinstance(current[k], dict):
                    current = current[k]
                else:
                    raise TypeError('Cannot overwrite key {}'.format(key))
            else:
                current[k] = value

            i += 1

    def get(self, key, default=None):
        """Get value from the registry.
        """
        current = self._storage
        parts = key.split('.')
        i = 1
        l = len(parts)
        for k in parts:
            if i < l:
                if k in current:
                    current = current[k]
                else:
                    return default
            else:
                if k in current:
                    return current[k]
                else:
                    return default
            i += 1

    def merge(self, other: dict):
        """Merges data into the registry.
        """
        self._storage = _util.dict_merge(self._storage, other)


class File(Memory):
    def __init__(self, root_dir, env_name: str):
        super().__init__()
        self.root_dir = root_dir
        self.env_name = env_name

        # Cascade load data from files
        for name in ('default.yml', env_name + '.yml'):
            file_path = _path.join(root_dir, name)
            if _path.isfile(file_path):
                with open(file_path) as f:
                    f_data = _yaml.load(f)
                    if isinstance(f_data, dict):
                        self.merge(f_data)
                    f.close()
