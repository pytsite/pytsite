"""PytSite Reload API Functions.
"""
from os import path as _path, utime as _utime
from pytsite import reg as _reg, logger as _logger, events as _events, console as _console, lang as _lang

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


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

    _logger.info('{} has been touched.'.format(touch_reload_path))

    _events.fire('pytsite.reload')

    if console_notify:
        _console.print_info(_lang.t('pytsite.reload@app_reloading'))
