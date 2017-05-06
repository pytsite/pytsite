"""PytSite Theme API
"""
from typing import Dict as _Dict
from importlib import import_module as _import_module
from os import path as _path, mkdir as _mkdir
from pytsite import reg as _reg, settings as _settings, logger as _logger, assetman as _assetman, reload as _reload
from . import _theme, _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_themes_path = _path.join(_reg.get('paths.root'), 'themes')

# Available themes
_themes = {}  # type: _Dict[str, _theme.Theme]

# Fallback theme
_fallback = None  # type: _theme.Theme

# Currently loaded theme
_loaded = None  # type: _theme.Theme


def get_themes_path():
    """Get absolute path to themes location.
    """
    return _themes_path


def get(name: str = None) -> _theme.Theme:
    """Get theme.
    """
    if not _themes:
        raise _error.NoThemesRegistered()

    if not name:
        if _loaded:
            return _loaded
        else:
            name = _settings.get('theme.current', _fallback.name)

    try:
        return _themes[name]
    except KeyError:
        raise _error.ThemeNotRegistered(name)


def switch(name: str):
    """Switch current theme.
    """
    if name not in _themes:
        raise _error.ThemeNotRegistered(name)

    # Switch only if it really necessary
    if name != get().name:
        _settings.put('theme.current', name)
        _settings.put('theme.compiled', False)
        _reload.reload()


def register(name: str):
    """Register a theme.
    """
    if name in _themes:
        raise _error.ThemeAlreadyRegistered(name)

    theme = _theme.Theme(name)
    _themes[name] = theme

    global _fallback
    if not _fallback:
        _fallback = theme


def get_registered() -> _Dict[str, _theme.Theme]:
    """Get registered themes.
    """
    return _themes


def load(name: str = None):
    """Load theme
    """
    global _loaded

    if _loaded:
        raise _error.ThemeLoadError("Cannot load theme '{}', because another theme '{}' is already loaded".
                                    format(name, _loaded.name))

    theme = get(name)

    # Create directories for resources
    for n in 'lang', 'tpl', 'assets':
        n_path = _path.join(theme.path, n)
        if not _path.exists(n_path):
            _mkdir(n_path, 0o755)

    # Register resources
    from pytsite import lang, tpl, assetman
    lang.register_package(theme.name, 'lang')
    tpl.register_package(theme.name, 'tpl')
    assetman.register_package(theme.name, 'assets')

    try:
        _import_module(theme.name)
        _loaded = theme
        _logger.info("Theme '{}' successfully loaded from '{}'".format(theme.name, theme.path))
    except ImportError as e:
        raise _error.ThemeLoadError("Error while loading theme package '{}': {}".format(theme.name, e))

    # Compile assets
    if _settings.get('theme.compiled') is False:
        _assetman.build(theme.name)
        _settings.put('theme.compiled', True)

    return theme
