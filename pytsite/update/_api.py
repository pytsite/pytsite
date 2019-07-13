"""PytSite Update API
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from typing import Callable
from semaver import Version
from pytsite import events


def on_update_stage_1(handler: Callable[[], None], priority: int = 0):
    """Shortcut
    """
    events.listen('pytsite.update@stage_1', handler, priority)


def on_update_stage_2(handler: Callable[[], None], priority: int = 0):
    """Shortcut
    """
    events.listen('pytsite.update@stage_2', handler, priority)


def on_update_pytsite(handler: Callable[[Version], None], priority: int = 0):
    """Shortcut
    """
    events.listen('pytsite.update@pytsite', handler, priority)


def on_update_app(handler: Callable[[Version], None], priority: int = 0):
    """Shortcut
    """
    events.listen('pytsite.update@app', handler, priority)


def on_update(handler: Callable[[dict], None], priority: int = 0):
    """Shortcut.
    """
    events.listen('pytsite.update@update', handler, priority)
