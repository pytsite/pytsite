"""PytSite Maintenance Mode API
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import console as _console, lang as _lang, cache as _cache

_cache_pool = _cache.create_pool('pytsite.maintenance')


def is_enabled() -> bool:
    """Check whether maintenance mode is enabled.
    """
    return _cache_pool.has('enabled')


def enable(silent: bool = False):
    """Enable maintenance mode.
    """
    if not is_enabled():
        _cache_pool.put('enabled', True)
        if not silent:
            _console.print_success(_lang.t('pytsite.maintenance@maintenance_mode_enabled'))


def disable(silent: bool = False):
    """Disable maintenance mode.
    """
    if is_enabled():
        _cache_pool.rm('enabled')
        if not silent:
            _console.print_success(_lang.t('pytsite.maintenance@maintenance_mode_disabled'))
