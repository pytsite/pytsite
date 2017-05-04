"""PytSite Reload API Functions.
"""
from os import path as _path
from pytsite import reg as _reg, events as _events, console as _console, lang as _lang, util as _util

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

RELOAD_MSG_ID = 'pytsite.reload@reload_required'
_flag = False


def reload():
    """Modify 'touch.reload' file.
    """
    touch_reload_path = _path.join(_reg.get('paths.storage'), 'touch.reload')

    _events.fire('pytsite.reload.before')

    with open(touch_reload_path, 'wt') as f:
        f.write(_util.w3c_datetime_str())

    _events.fire('pytsite.reload')

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
