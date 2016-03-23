"""PytSite Threading.
"""
import threading as _threading

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def get_id() -> int:
    """Get current thread ID.
    """
    return _threading.get_ident()


def create(target, **kwargs) -> _threading.Thread:
    """Create a thread.
    """
    return _threading.Thread(target=target, kwargs=kwargs)


def active_count() -> int:
    """Get number of active threads.
    """
    return _threading.active_count()
