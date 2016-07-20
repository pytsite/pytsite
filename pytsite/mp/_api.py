"""PytSite Multiprocessing API.
"""
from pytsite import reg as _reg
from . import _lock, _redis

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_driver_name = _reg.get('mp.locks.driver', 'redis')


def get_lock(name: str, re_entrant: bool = False, driver: str = _driver_name) -> _lock.Abstract:
    """Lock factory.
    """
    # Ask driver to create lock object
    if driver == 'redis':
        return _redis.Lock(name, re_entrant)
    else:
        raise KeyError('Unsupported lock driver: {}'.format(driver))
