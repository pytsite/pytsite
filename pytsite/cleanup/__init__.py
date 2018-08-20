"""PytSite Cleanup
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import cron as _cron, events as _events
from . import _eh


# Public API
def on_cleanup(handler, priority: int = 0):
    _events.listen('pytsite.cleanup@cleanup', handler, priority)


# Events handlers
_cron.hourly(_eh.cron_hourly)
