"""Pytsite Robots Module.
"""
from pytsite import events as _events
from . import _eh

# Public API
from ._api import disallow, sitemap

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


_events.listen('pytsite.cron.daily', _eh.cron_daily)
