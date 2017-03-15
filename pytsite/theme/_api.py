"""PytSite Theme API
"""
from typing import Dict as _Dict
from os import path as _path
from pytsite import reg as _reg
from . import _theme, _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_themes_path = _path.join(_reg.get('paths.root'), 'themes')

# Available themes
_themes = {}  # type: _Dict[str, _theme.Theme]

# Default theme
_default = None  # type: _theme.Theme


def get_themes_path():
    """Get absolute path of themes location.
    """
    return _themes_path


def set_default(theme: _theme.Theme):
    """Set current theme.
    """
    global _default

    _default = theme


def register(package_name: str):
    """Register a theme.
    """
    if package_name in _themes:
        raise RuntimeError("Theme '{}' is already registered".format(package_name))

    theme = _theme.Theme(package_name)
    _themes[package_name] = theme

    # Set first registered theme as default
    if len(_themes) == 1:
        set_default(theme)


def get_all() -> _Dict[str, _theme.Theme]:
    """Get all available themes.
    """
    return _themes


def get(package_name: str = None) -> _theme.Theme:
    """Get theme.
    """
    if not _themes:
        raise _error.NoThemesRegistered('There is no themes registered')

    if not package_name:
        return _default
    elif package_name not in _themes:
        raise _error.ThemeNotRegistered("Theme '{}' is not registered".format(package_name))

    return _themes[package_name]
