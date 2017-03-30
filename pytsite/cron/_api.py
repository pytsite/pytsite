"""PytSite Cron API
"""
from pytsite import events as _events

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def every_min(handler, priority: int = 0):
    _events.listen('pytsite.cron.1min', handler, priority)


def every_5min(handler, priority: int = 0):
    _events.listen('pytsite.cron.5min', handler, priority)


def every_15min(handler, priority: int = 0):
    _events.listen('pytsite.cron.15min', handler, priority)


def every_30min(handler, priority: int = 0):
    _events.listen('pytsite.cron.30min', handler, priority)


def hourly(handler, priority: int = 0):
    _events.listen('pytsite.cron.hourly', handler, priority)


def daily(handler, priority: int = 0):
    _events.listen('pytsite.cron.daily', handler, priority)


def weekly(handler, priority: int = 0):
    _events.listen('pytsite.cron.weekly', handler, priority)


def monthly(handler, priority: int = 0):
    _events.listen('pytsite.cron.monthly', handler, priority)
