"""PytSite Threading API
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from typing import Union, Optional
from threading import Thread as PythonThread, current_thread
from ._thread import Thread
from ._timer import Timer


def get_id() -> int:
    """Get current thread ID
    """
    return current_thread().ident


def get_parent_id() -> Optional[int]:
    """Get parent thread ID
    """
    t = current_thread()  # type: Union[Thread, Timer, PythonThread]
    return t.parent.ident if isinstance(t, (Thread, Timer)) else None


def create_thread(target, **kwargs) -> Thread:
    """Create a new thread
    """
    return Thread(target=target, kwargs=kwargs)


def create_timer(target, delay: float, **kwargs) -> Timer:
    """Create a new timer
    """
    return Timer(delay, target, kwargs=kwargs)


def run_in_thread(target, delay: float = 0.0, **kwargs) -> Timer:
    """Run target in a thread
    """
    thread = create_timer(target, delay, **kwargs)
    thread.start()

    return thread
