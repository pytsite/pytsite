from abc import ABC, abstractmethod
from os import path

from pytsite.core import helpers


class ConfigDriver(ABC):
    _storage = dict()

    @abstractmethod
    def set_val(self, key: str, value):
        """Set value of the registry.
        """
        pass

    @abstractmethod
    def get_val(self, key: str, default):
        """Get value from the registry.
        """
        pass

    @abstractmethod
    def merge(self, other: dict):
        """Merge other dictionary onto the registry storage.
        """
        pass

    def get_all(self)->dict:
        """Get all registry's content.
        """
        return self._storage


class MemoryDriver(ConfigDriver):
    def set_val(self, key: str, value):
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
                    raise TypeError('Cannot overwrite {0}', key)
            else:
                current[k] = value

            i += 1

    def get_val(self, key, default=None):
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
        self._storage = helpers.dict_merge(self._storage, other)


class FileDriver(MemoryDriver):
    def __init__(self, root_dir, env_name: str):
        super().__init__()
        self.root_dir = root_dir
        self.env_name = env_name

        import yaml
        for name in ('default.yml', env_name + '.yml'):
            file_path = root_dir + path.sep + name
            if path.isfile(file_path):
                file = open(file_path, 'r')
                self.merge(yaml.load(file))
                file.close()

    def get_val(self, key: str, default=None):
        """Get value from the registry.
        """
        return super().get_val(key, default)


# Default driver
__current_driver = MemoryDriver()


def set_driver(driver: ConfigDriver):
    """Switch registry driver"""
    global __current_driver
    __current_driver = driver


def set_val(key: str, value):
    """Set registry's value"""
    __current_driver.set_val(key, value)


def get_val(key: str, default=None):
    """Get registry's value"""
    return __current_driver.get_val(key, default)


def get_all()->dict:
    """Get all registry's content"""
    return __current_driver.get_all()


def merge(other: dict):
    __current_driver.merge(other)