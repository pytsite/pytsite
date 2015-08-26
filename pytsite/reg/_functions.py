"""PytSite Registry Functions.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


from .driver import Abstract as _RegistryDriver, Memory as _MemoryDriver

# Default driver
__current_driver = _MemoryDriver()


def set_driver(driver: _RegistryDriver):
    """Switch registry driver.
    """
    global __current_driver
    __current_driver = driver


def set_val(key: str, value):
    """Set registry's value.
    """
    __current_driver.set_val(key, value)


def get(key: str, default=None):
    """Get registry's value.
    """
    return __current_driver.get_val(key, default)


def get_all()->dict:
    """Get all registry's content.
    """
    return __current_driver.get_all()


def merge(other: dict):
    __current_driver.merge(other)
