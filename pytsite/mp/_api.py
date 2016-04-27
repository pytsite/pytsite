"""PytSite Multiprocessing API.
"""
from pytsite import reg as _reg, util as _util
from . import _lock

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_locks = {}
_default_driver = _reg.get('mp.locks.driver', 'redis')


def get_lock(name: str = None, recursive: bool = False, driver: str = _default_driver) -> _lock.Abstract:
    """Lock factory.
    """
    if not name:
        name = _util.random_str(exclude=_locks.keys())

    if name in _locks:
        return _locks[name]

    if driver == 'redis':
        l = _lock.Redis(name, recursive)
    else:
        raise KeyError('Unsupported lock driver: {}'.format(driver))

    _locks[name] = l

    return l
