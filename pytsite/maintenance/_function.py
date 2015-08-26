"""Maintenance Functions.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from datetime import datetime as _datetime
from os import unlink as _unlink, path as _path
from pytsite import reg as _reg

_lock_path = _reg.get('paths.maintenance.lock')


def is_enabled() -> bool:
    return _path.exists(_lock_path)


def enable():
    if not is_enabled():
        with open(_lock_path, 'wt') as f:
            f.write(str(_datetime.now()))


def disable():
    if is_enabled():
        _unlink(_lock_path)
