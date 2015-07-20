"""PytSite Cache.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from os import path as _path
from beaker import util as _beaker_util, cache as _beaker_cache
from . import reg as _reg

_cache_manager = None
""":type: beaker.cache.CacheManager"""


def _init():
    """Init.
    """
    global _cache_manager

    if _cache_manager:
        return

    allowed_types = ('file', 'memcached')
    cache_type = _reg.get('cache.type', 'file')

    if cache_type not in allowed_types:
        raise Exception("Invalid cache type: {}. Allowed types are: {}.".format(cache_type, str(allowed_types)))

    default_data_dir = _path.join(_reg.get('paths.tmp'), 'cache')
    default_lock_dir = _path.join(default_data_dir, 'lock')

    config = {
        'cache.type': cache_type,
        'cache.data_dir': _reg.get('cache.data_dir', default_data_dir),
        'cache.lock_dir': _reg.get('cache.lock_dir', default_lock_dir),
    }

    if cache_type == 'memcached':
        config['cache.url'] = _reg.get('cache.url', 'localhost:11211')

    _cache_manager = _beaker_cache.CacheManager(**_beaker_util.parse_cache_config_options(config))


def put(key: str, value, **kwargs):
    """Put a value to the cache.
    """
    return _cache_manager.get_cache('pytsite').put(key, value, **kwargs)


def has(key: str) -> bool:
    """Checks if the cache contains value.
    """
    return _cache_manager.get_cache('pytsite').has_key(key)


def get(key: str, **kwargs):
    """Retrieve a cached value from the cache.
    """
    return _cache_manager.get_cache('pytsite').get(key, **kwargs)


def rm(key: str, **kwargs):
    """Remove value from the cache.
    """
    return _cache_manager.get_cache('pytsite').remove_value(key, **kwargs)


_init()
