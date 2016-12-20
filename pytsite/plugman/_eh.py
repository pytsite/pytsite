"""PytSite Plugman Event Handlers
"""
from os import path as _path, listdir as _listdir
from shutil import move as _move, rmtree as _rmtree
from pytsite import reg as _reg, console as _console, lang as _lang
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def update(version: str):
    """pytsite.update
    """
    if version == '0.95.0':
        _update_0_95_5()


def update_after():
    for name, info in _api.get_plugins().items():
        if info.get('upgradable'):
            _console.print_info(_lang.t('pytsite.plugman@upgrading_plugin', {
                'name': name,
                'old_ver': info['installed_version'],
                'new_ver': info['latest_version'],
            }))
            _api.upgrade(name)


def _update_0_95_5():
    # Move plugins to the new location
    old_plugins_path = _path.join(_reg.get('paths.app'), 'plugins')
    if not _path.isdir(old_plugins_path):
        return

    for name in _listdir(old_plugins_path):
        new_plugins_path = _api.get_plugins_path()
        src = _path.join(old_plugins_path, name)
        dst = _path.join(new_plugins_path, name)

        if _path.exists(dst):
            continue

        _move(src, dst)
        _console.print_info('{} moved to {}'.format(src, dst))

    _rmtree(old_plugins_path)
    _console.print_info('{} has been deleted'.format(old_plugins_path))
