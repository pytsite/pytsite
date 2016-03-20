"""PytSite Threading.
"""
import threading as _threading

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def create_thread(target, **kwargs) -> _threading.Thread:
    return _threading.Thread(target=target, kwargs=kwargs)


def active_count() -> int:
    return _threading.active_count()
