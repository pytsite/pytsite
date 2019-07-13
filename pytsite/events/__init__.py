"""PytSite Events
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import re as _re
from typing import List, Tuple, Callable, Any, Pattern

_LISTENERS = []


def listen(event_name: str, handler: callable, priority: int = 0):
    """Add an event listener.
    """
    global _LISTENERS

    re = _re.compile(event_name.replace('.', '\\.').replace('*', '.*?') + '$')
    _LISTENERS.append((handler, priority, re))
    _LISTENERS = sorted(_LISTENERS, key=lambda x: x[1])  # Sort by priority


def listeners(event_name: str) -> List[Tuple[Callable[..., Any], int, Pattern]]:
    """Get listeners of the event
    """
    r = []

    for handler, priority, re in _LISTENERS:
        if re.match(event_name):
            r.append((handler, priority, re))

    return r


def fire(event_name: str, _concurrent: bool = False, _wait: bool = True, _stop_after: int = None, **kwargs) -> list:
    """Fires an event to listeners
    """
    r = []
    q = None

    if _concurrent:
        from pytsite import queue
        q = queue.Queue('pytsite.events')

    count = 0
    for handler, priority, re in listeners(event_name):
        if _concurrent:
            # Queue handler
            q.put(handler, **kwargs)
        else:
            # Call handler and append its result to return value
            r.append(handler(**kwargs))

        # Count called handler and stop if it is necessary
        count += 1
        if _stop_after and count >= _stop_after:
            break

    if q:
        q.execute(_wait)

    return r


def first(event: str, _concurrent: bool = False, _wait: bool = True, **kwargs):
    """Fires an event and process only one handler
    """
    r = fire(event, _concurrent, _wait, 1, **kwargs)

    return r[0] if r else None
