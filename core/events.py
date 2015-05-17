"""Events.
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


def fire(event: str, **kwargs):
    """Fires an event to listeners.
    """

    print(event)

    global __listeners
    if event in __listeners:
        for handler in __listeners[event].values:
            handler(**kwargs)
