"""Event Subsystem.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

__listeners = {}


def listen(event: str, listener: callable, call_once: bool=False):
    """Add an event listener.
    """
    global __listeners
    if event not in __listeners:
        __listeners[event] = []

    __listeners[event].append((listener, call_once))


def fire(event: str, stop_after: int=None, **kwargs):
    """Fires an event to listeners.
    """
    if event not in __listeners:
        return

    count = 0
    for handler, call_once in __listeners[event]:
        handler(**kwargs)
        count += 1
        if stop_after and count >= stop_after:
            break

    # Remove handlers which should be called once
    __listeners[event] = [item for item in __listeners[event] if not item[1]]


def first(event: str, **kwargs):
    """Fires an event and process only one handler.
    """
    return fire(event, stop_after=1, **kwargs)
