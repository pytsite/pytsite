"""PytSite Cache
"""
from pytsite import events as _events
from ._api import set_driver, has_pool, create_pool, get_pool, cleanup
from . import _driver as driver, _error as error
from ._pool import Pool

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

set_driver(driver.File())
_events.listen('pytsite.cron@1min', cleanup)
