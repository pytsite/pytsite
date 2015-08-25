"""PytSite Threading.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import threading as _threading

__lock = _threading.Lock()
__r_lock = _threading.RLock()


def get_lock():
    return __lock


def get_r_lock():
    return __r_lock


def create_thread(target, **kwargs) -> _threading.Thread:
    return _threading.Thread(target=target, kwargs=kwargs)


def active_count() -> int:
    return _threading.active_count()
