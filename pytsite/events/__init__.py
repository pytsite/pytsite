"""Event Subsystem.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

__listeners = {}


def listen(event: str, listener: callable):
    """Add an event listener.
    """
    global __listeners
    if event not in __listeners:
        __listeners[event] = []

    __listeners[event].append(listener)


def fire(event: str, stop_after: int=None, **kwargs: dict):
    """Fires an event to listeners.
    """
    if event not in __listeners:
        return

    count = 0
    for handler in __listeners[event]:
        handler(**kwargs)
        count += 1
        if stop_after and count >= stop_after:
            return


def first(event: str, **kwargs: dict):
    """Fires an event and process only one handler.
    """
    return fire(event, stop_after=1, **kwargs)
