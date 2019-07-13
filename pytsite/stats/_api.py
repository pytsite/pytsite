"""PytSite Stats API Functions
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import events


def on_update(handler):
    events.listen('pytsite.stats@update', handler)
