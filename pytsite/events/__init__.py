"""Events Subsystem
"""
import re as _re
from pytsite import reg as _reg, logger as _logger

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_listeners = []
_dbg = _reg.get('events.debug', False)


def listen(event_name: str, handler: callable, priority: int = 0):
    """Add an event listener.
    """
    global _listeners

    re = _re.compile(event_name.replace('.', '\.').replace('*', '.*?') + '$')
    _listeners.append((handler, priority, re))
    _listeners = sorted(_listeners, key=lambda x: x[1])  # Sort by priority

    if _dbg:
        _logger.debug('Listener {}.{}() attached to event {}'.format(event_name, handler.__module__, handler.__name__))


def fire(event_name: str, stop_after: int = None, **kwargs) -> list:
    """Fires an event to listeners.
    """
    count = 0
    r = []

    for handler, priority, re in _listeners:
        if not re.match(event_name):
            continue

        # Call handler and append its result to return value
        r.append(handler(**kwargs))

        # Count called handler and stop if it is necessary
        count += 1
        if stop_after and count >= stop_after:
            break

    return r


def first(event: str, **kwargs):
    """Fires an event and process only one handler.
    """
    return fire(event, stop_after=1, **kwargs)
