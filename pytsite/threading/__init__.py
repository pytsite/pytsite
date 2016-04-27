"""PytSite Threading.
"""
import threading as _threading

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


_lock = _threading.Lock()
_r_lock = _threading.RLock()


def get_id() -> int:
    """Get current thread ID.
    """
    return _threading.get_ident()


def create_thread(target, **kwargs) -> _threading.Thread:
    """Create a thread.
    """
    return _threading.Thread(target=target, kwargs=kwargs)


def get_lock():
    """Get lock.
    """
    return _lock


def get_r_lock():
    """Get reentrant lock.
    """
    return _r_lock


def active_count() -> int:
    """Get number of active threads.
    """
    return _threading.active_count()
