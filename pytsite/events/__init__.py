"""Event Subsystem.
"""
from pytsite import reg as _reg, logger as _logger

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_listeners = {}
_dbg = _reg.get('events.debug', False)


def listen(event: str, listener: callable, call_once: bool = False, priority: int = 0):
    """Add an event listener.
    """
    global _listeners
    if event not in _listeners:
        _listeners[event] = []

    _listeners[event].append((listener, call_once, priority))

    # Sort listeners by priority
    _listeners[event] = sorted(_listeners[event], key=lambda x: x[2])

    if _dbg:
        _logger.debug("Listener attached to event '{}': {}.{}()".format(event, listener.__module__, listener.__name__))


def fire(event: str, stop_after: int = None, **kwargs):
    """Fires an event to listeners.
    """
    if event not in _listeners:
        return

    count = 0
    for handler, call_once, priority in _listeners[event]:
        # Call handler
        handler(**kwargs)

        # Count called handler and stop if it is necessary
        count += 1
        if stop_after and count >= stop_after:
            break

    # Remove handlers which should be called once
    _listeners[event] = [item for item in _listeners[event] if not item[1]]


def first(event: str, **kwargs):
    """Fires an event and process only one handler.
    """
    return fire(event, stop_after=1, **kwargs)
