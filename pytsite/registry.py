from abc import ABC, abstractmethod
from easydict import EasyDict

class ConfigDriver(ABC):
    _storage = dict()

    @abstractmethod
    def set_val(self, key, value):
        pass

    @abstractmethod
    def get_val(self, key, default):
        pass

    @abstractmethod
    def get_all(self):
        pass


class MemoryDriver(ConfigDriver):
    def set_val(self, key, value):
        self._storage[key] = value

    def get_val(self, key, default=None):
        if key in self._storage:
            return self._storage[key]
        return default

    def get_all(self):
        return self._storage


class FileDriver(MemoryDriver):
    def __init__(self, root_dir):
        super().__init__()
        self.root_dir = root_dir

    def get_val(self, key, default=None):
        import yaml
        d = yaml.load('test.yml')
        print(d)

""" :type: ConfigDriver """
__current_drv = MemoryDriver()


def set_driver(driver: ConfigDriver):
    __current_drv = driver


def set_val(key: str, value):
    __current_drv.set_val(key, value)


def get_val(key, default=None):
    return __current_drv.get_val(key, default)

def get_all():
    return __current_drv.get_all()