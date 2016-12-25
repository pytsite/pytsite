"""PytSite Core Event Handlers.
"""
from shutil import move as _move
from os import path as _path, listdir as _listdir, makedirs as _makedirs, rmdir as _rmdir
from pytsite import reg as _reg, console as _console

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def update(version: str):
    if version == '0.98.25':
        _update_0_98_25()


def _update_0_98_25():
    app_d = _reg.get('paths.app')
    for d in 'config', 'log', 'storage', 'tmp':
        src_d = _path.join(app_d, d)
        if not _path.isdir(src_d):
            continue

        dst_d = _path.join(_reg.get('paths.root'), d)
        _makedirs(dst_d, 0o755, True)

        for a in _listdir(src_d):
            _move(_path.join(src_d, a), _path.join(dst_d, a))

        _rmdir(src_d)

        _console.print_info('{} moved to {}'.format(src_d, dst_d))
