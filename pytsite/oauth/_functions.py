"""oAuth Functions.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import auth
from pytsite.core import odm as _odm
from . import _driver

__drivers = {}


def register_driver(name: str, title: str, driver_cls: type):
    """Register oAuth driver.
    """
    if name in __drivers:
        raise KeyError("Driver with name '{}' already registered.")

    if not issubclass(driver_cls, _driver.Abstract):
        raise ValueError("Invalid driver's class.")

    __drivers[name] = (title, driver_cls)


def get_drivers() -> dict:
    """Get registered drivers.
    """
    return __drivers


def get_driver(name: str) -> tuple:
    """Get info about registered driver.
    """
    if name not in __drivers:
        raise KeyError("Driver '{}' is not registered.".format(name))

    return __drivers[name]


def load_driver(name: str, **kwargs) -> _driver.Abstract:
    """Instantiate driver.
    """
    return get_driver(name)[1](**kwargs)


def get_accounts(owner: auth.model.User=None):
    """Get existing oAuth accounts.
    :rtype: list[pytsite.oauth._model.Account]
    """
    f = _odm.find('oauth_account')
    if owner:
        f.where('owner', '=', owner)

    return list(f.get())
