"""PytSite Cache
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

# Public API
from ._api import set_driver, has_pool, create_pool, get_pool, cleanup
from . import _driver as driver, _error as error
from ._pool import Pool

from pytsite import reg as _reg, threading as _threading

if _reg.get('env.type') == 'uwsgi':
    def _cleanup_worker():
        cleanup()
        _threading.run_in_thread(_cleanup_worker, 60)


    _threading.run_in_thread(_cleanup_worker, 60)
