"""PytSite Cache
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

# Public API
from ._api import set_driver, has_pool, create_pool, get_pool, get_pools, cleanup
from . import _driver as driver, _error as error
from ._pool import Pool

from pytsite import reg as _reg, threading as _threading, update as _update, semver as _semver

if _reg.get('env.type') == 'wsgi':
    def _cleanup_worker():
        cleanup()
        _threading.run_in_thread(_cleanup_worker, 60)


    _threading.run_in_thread(_cleanup_worker, 60)


def _update_pytsite(v_from: _semver.Version):
    if v_from <= '7.9':
        from os import path
        from shutil import rmtree

        # New dict key added to all file storage items, so entire file cache must be cleared
        rmtree(_reg.get('cache.file_driver_storage', path.join(_reg.get('paths.storage'), 'cache')))


_update.on_update_pytsite(_update_pytsite)
