from abc import ABC, abstractmethod
from os import path

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
        print('a')
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
        d = yaml.load(open(self.root_dir + path.sep + 'test.yml', 'r'))
        print(d)


class Registry:
    def __init__(self):
        self.__current_drv = MemoryDriver()

    def set_driver(self, driver: ConfigDriver):
        self.__current_drv = driver

    def set_val(self, key: str, value):
        self.__current_drv.set_val(key, value)

    def get_val(self, key: str, default=None):
        return self.__current_drv.get_val(key, default)

    def get_all(self)->list:
        return self.__current_drv.get_all()