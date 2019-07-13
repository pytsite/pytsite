"""PytSite Reload API Functions
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from os import path as path
from pytsite import reg, events, console, lang, util, threading

RELOAD_MSG_ID = 'pytsite.reload@reload_required'
_flag = False


def _do_reload():
    """Modify 'touch.reload' file
    """
    touch_reload_path = path.join(reg.get('paths.storage'), 'touch.reload')

    events.fire('pytsite.reload@before_reload')

    with open(touch_reload_path, 'wt') as f:
        f.write(util.w3c_datetime_str())

    events.fire('pytsite.reload@reload')

    console.print_info(lang.t('pytsite.reload@app_is_reloading'))


def reload(delay: float = 0.0):
    """Request reload
    """
    threading.run_in_thread(_do_reload, delay)


def on_before_reload(handler, priority: int = 0):
    """Shortcut
    """
    events.listen('pytsite.reload@before_reload', handler, priority)


def on_reload(handler, priority: int = 0):
    """Shortcut
    """
    events.listen('pytsite.reload@reload', handler, priority)


def set_flag():
    """Set 'Reload request' flag state
    """
    global _flag

    _flag = True


def get_flag() -> bool:
    """Get 'Reload request' flag state
    """
    return _flag
