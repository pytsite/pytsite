"""PytSite Registry Drivers
"""
import yaml as _yaml
from os import path as _path
from abc import ABC as _ABC, abstractmethod as _abstractmethod
from pytsite import util as _util

__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Abstract(_ABC):
    """PytSite Abstract Registry Driver
    """

    def __init__(self, parent=None):
        """
        :type parent: Abstract
        """
        self._parent = parent

    @_abstractmethod
    def _put(self, key: str, value):
        """Put a value into the registry
        """
        pass

    def put(self, key: str, value):
        """Put a value into the registry
        """
        self._put(key, value)

    @_abstractmethod
    def _get(self, key: str):
        """Get value from the registry
        """
        pass

    def get(self, key: str, default=None):
        """Get value from the registry
        """
        value = self._get(key)

        if value is None:
            return self._parent.get(key, default) if self._parent else default

        return value


class Memory(Abstract):
    """PytSite Memory Registry Driver
    """

    def __init__(self, parent: Abstract = None):
        super().__init__(parent)

        self._storage = {}

    def _put(self, key: str, value):
        """Put a value into the registry
        """
        current_storage_dict = self._storage
        sub_keys = key.split('.')
        i = 1
        length = len(sub_keys)
        for sub_key in sub_keys:
            if i < length:
                if sub_key not in current_storage_dict:
                    current_storage_dict[sub_key] = dict()
                    current_storage_dict = current_storage_dict[sub_key]
                elif sub_key in current_storage_dict and isinstance(current_storage_dict[sub_key], dict):
                    current_storage_dict = current_storage_dict[sub_key]
                else:
                    raise TypeError('Cannot overwrite key {}'.format(key))

            else:
                current_storage_dict[sub_key] = value

            i += 1

    def _get(self, key):
        """Get a value from the registry
        """
        current_storage_dict = self._storage
        sub_keys = key.split('.')
        i = 1
        sub_keys_count = len(sub_keys)
        for sub_key in sub_keys:
            if i < sub_keys_count:
                if sub_key in current_storage_dict:
                    current_storage_dict = current_storage_dict[sub_key]
                else:
                    return

            else:
                if sub_key in current_storage_dict:
                    return current_storage_dict[sub_key]
                else:
                    return

            i += 1


class File(Memory):
    def __init__(self, root_dir, env_name: str, parent: Abstract = None):
        super().__init__(parent)

        self.root_dir = root_dir
        self.env_name = env_name

        # Load data from files
        for name in ('default.yml', env_name + '.yml'):
            file_path = _path.join(root_dir, name)
            if _path.isfile(file_path):
                with open(file_path) as f:
                    f_data = _yaml.load(f)
                    if isinstance(f_data, dict):
                        self._merge(f_data)
                    f.close()

    def _merge(self, other: dict):
        """Merges data into the registry.
        """
        self._storage = _util.dict_merge(self._storage, other)
