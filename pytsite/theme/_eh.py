"""PytSite Theme Event Handlers.
"""
from os import path as _path
from shutil import move as _move
from pytsite import settings as _settings, reg as _reg, console as _console, file as _file, metatag as _metatag
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def router_dispatch():
    """pytsite.router.dispatch
    """
    # Set favicon URL
    favicon_fid = _settings.get('theme.favicon_fid')
    if favicon_fid:
        try:
            f = _file.get(favicon_fid)
            _metatag.rm('link', rel='icon')
            _metatag.t_set('link', rel='icon', type=f.mime, href=f.get_url(width=50, height=50))
        except _file.error.FileNotFound:
            pass


def update(version: str):
    """pytsite.update
    """
    if version == '0.95.0':
        # Move themes to the new location
        old_themes_path = _path.join(_reg.get('paths.app'), 'themes')
        new_themes_path = _api.get_themes_path()
        if _path.isdir(old_themes_path) and not _path.isdir(new_themes_path):
            _move(old_themes_path, new_themes_path)
            _console.print_info('{} moved to {}'.format(old_themes_path, new_themes_path))
