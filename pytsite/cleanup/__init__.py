"""PytSite Cleanup Module.
"""
from pytsite import cron as _cron
from ._eh import cron_hourly

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_cron.hourly(cron_hourly)
