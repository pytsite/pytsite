"""PytSite Cache.
"""
from pytsite import events as _events
from ._api import has_pool, create_pool, get_pool, clear_pool, delete_pool, cleanup_pools
from . import _driver as driver, _error as error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_events.listen('pytsite.cron.1min', cleanup_pools)
