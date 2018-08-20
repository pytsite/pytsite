"""PytSite Threading
"""
import threading as _python_threading
from threading import Thread, Timer

__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def get_id() -> int:
    """Get current thread ID
    """
    return _python_threading.get_ident()


def active_count() -> int:
    """Get number of active threads
    """
    return _python_threading.active_count()


def create_thread(target, **kwargs) -> Thread:
    """Create a thread
    """
    return Thread(target=target, kwargs=kwargs)


def create_timer(target, delay: float, **kwargs) -> Timer:
    """Create a timer
    """
    return Timer(delay, target, kwargs=kwargs)


def run_in_thread(target, delay: float = 0.0, **kwargs):
    """Run target in thread
    """
    thread = create_timer(target, delay, **kwargs)
    thread.start()

    return thread
