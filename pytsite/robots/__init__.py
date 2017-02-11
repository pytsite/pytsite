"""Pytsite robots.txt support.
"""

# Public API
from ._api import disallow, sitemap

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import cron
    from . import _eh

    cron.daily(_eh.cron_daily)


_init()
