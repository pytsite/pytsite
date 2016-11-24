"""PytSite Theme Event Handlers.
"""
from os import path as _path
from shutil import move as _move
from pytsite import http as _http, router as _router, settings as _settings, reg as _reg, console as _console
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def router_dispatch():
    """pytsite.router.dispatch
    """
    request_input = _router.request().inp
    request_cookies = _router.request().cookies
    theme_setting = _settings.get('theme.default_theme')

    # Change theme from input, cookie or settings
    if '__theme' in request_input and _api.is_registered(request_input['__theme']):
        _api.set_current(request_input['__theme'])
    elif 'PYTSITE_THEME' in request_cookies and _api.is_registered(request_cookies['PYTSITE_THEME']):
        _api.set_current(request_cookies['PYTSITE_THEME'])
    elif theme_setting and _api.is_registered(theme_setting):
        _api.set_current(theme_setting)


def router_response(response: _http.response.Response):
    """pytsite.router.response
    """
    request_input = _router.request().inp

    # Store selected theme in cookie
    if '__theme' in request_input and _api.is_registered(request_input['__theme']):
        response.set_cookie('PYTSITE_THEME', request_input['__theme'])


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
