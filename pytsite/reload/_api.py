"""PytSite Reload API Functions.
"""
from os import path as _path, utime as _utime
from pytsite import reg as _reg, logger as _logger, events as _events, console as _console, lang as _lang

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

RELOAD_MSG_ID = 'pytsite.reload@reload_required'
_flag = False


def reload(console_notify: bool = True):
    """Touch 'touch.reload' file.
    """
    touch_reload_path = _path.join(_reg.get('paths.storage'), 'touch.reload')

    _events.fire('pytsite.reload.before')

    if not _path.exists(touch_reload_path):
        with open(touch_reload_path, 'w'):
            pass
    else:
        _utime(touch_reload_path, None)

    _events.fire('pytsite.reload')

    _logger.info('Application is reloading')

    if console_notify:
        _console.print_info(_lang.t('pytsite.reload@app_is_reloading'))


def set_flag():
    """Set 'Reload requested' flag state.
    """
    global _flag

    _flag = True


def get_flag() -> bool:
    """Get 'Reload requested' flag state.
    """
    return _flag
