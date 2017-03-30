"""Event Subsystem.
"""
import re as _re
from pytsite import reg as _reg, logger as _logger

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_listeners = {}  # Listeners for exact event names
_wc_listeners = []  # Listeners for wildcard event names
_dbg = _reg.get('events.debug', False)


def listen(event_name: str, listener: callable, priority: int = 0):
    """Add an event listener.
    """
    global _listeners, _wc_listeners

    # Exact event name
    if not event_name.endswith('*'):
        if event_name not in _listeners:
            _listeners[event_name] = []
        _listeners[event_name].append((listener, priority))
        _listeners[event_name] = sorted(_listeners[event_name], key=lambda x: x[1])  # Sort by priority

    # Wildcard event name
    else:
        re = _re.compile(event_name.replace('.', '\.').replace('*', '.*'))
        _wc_listeners.append((listener, priority, re))
        _wc_listeners = sorted(_wc_listeners, key=lambda x: x[1])  # Sort by priority

    if _dbg:
        _logger.debug('Listener {}.{}() attached to event {}'.format(event_name, listener.__module__, listener.__name__))


def fire(event_name: str, stop_after: int = None, **kwargs) -> list:
    """Fires an event to listeners.
    """
    count = 0
    stop_processing = False
    r = []

    # Call listeners for exact event name
    if event_name in _listeners:
        for handler, priority in _listeners[event_name]:
            # Call handler
            r.append(handler(**kwargs))

            # Count called handler and stop if it is necessary
            count += 1
            if stop_after and count >= stop_after:
                stop_processing = True
                break

    # Call listeners for exact event name
    if not stop_processing:
        for handler, priority, re in _wc_listeners:
            if not re.match(event_name):
                continue

            # Call handler
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
