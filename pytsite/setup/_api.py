"""PytSite Setup Functions.
"""
from os import path as _path
from pytsite import reg as _reg, events as _events

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def is_setup_completed() -> bool:
    """Check if the setup was performed.
    """
    return _path.exists(_reg.get('paths.setup.lock'))


def on_setup(handler, priority: int = 0):
    """Add a listener for 'pytsite.setup' event.
    """
    _events.listen('pytsite.setup', handler, priority)
