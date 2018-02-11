"""PytSite Update API
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from typing import Callable as _Callable
from pytsite import events as _events


def on_update_stage_1(handler: _Callable[[dict], None], priority: int = 0):
    """Shortcut
    """
    _events.listen('pytsite.update@stage_1', handler, priority)


def on_update_stage_2(handler: _Callable[[dict], None], priority: int = 0):
    """Shortcut
    """
    _events.listen('pytsite.update@stage_2', handler, priority)


def on_update(handler: _Callable[[dict], None], priority: int = 0):
    """Shortcut.
    """
    _events.listen('pytsite@update', handler, priority)
