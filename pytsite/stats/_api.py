"""PytSite Stats API
"""
from pytsite import events as _events

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def on_update(handler):
    _events.listen('pytsite.stats.update', handler)
