"""PytSite Threading
"""
import threading as _python_threading
from threading import RLock, Thread, Timer

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

# Ready to use re-entrant lock
_shared_r_lock = RLock()


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


def create_timer(target, timeout: float, **kwargs) -> Timer:
    """Create a timer
    """
    return Timer(timeout, target, kwargs=kwargs)


def create_r_lock():
    """Create re-entrant lock
    """
    return RLock()


def get_shared_r_lock():
    """Get shared re-entrant lock
    """
    return _shared_r_lock
