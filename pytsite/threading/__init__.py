"""PytSite Threading.
"""
import threading as _python_threading

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


_shared_r_lock = _python_threading.RLock()


def get_id() -> int:
    """Get current thread ID.
    """
    return _python_threading.get_ident()


def create_thread(target, **kwargs) -> _python_threading.Thread:
    """Create a thread.
    """
    return _python_threading.Thread(target=target, kwargs=kwargs)


def create_r_lock():
    return _python_threading.RLock()


def get_shared_r_lock():
    """Get re-entrant lock.
    """
    return _shared_r_lock


def active_count() -> int:
    """Get number of active threads.
    """
    return _python_threading.active_count()
