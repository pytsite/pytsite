"""PytSite Maintenance Mode API.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from datetime import datetime as _datetime
from os import unlink as _unlink, path as _path
from pytsite import reg as _reg, console as _console, lang as _lang

_lock_path = _reg.get('paths.maintenance.lock')


def is_enabled() -> bool:
    """Check whenter maintenance mode is enabled.
    """
    return _path.exists(_lock_path)


def enable():
    """Enable maintenance mode.
    """
    if not is_enabled():
        with open(_lock_path, 'wt') as f:
            f.write(str(_datetime.now()))
        _console.print_success(_lang.t('pytsite.maintenance@maintenance_mode_enabled'))


def disable():
    """Disable maintenance mode.
    """
    if is_enabled():
        _unlink(_lock_path)
        _console.print_success(_lang.t('pytsite.maintenance@maintenance_mode_disabled'))
