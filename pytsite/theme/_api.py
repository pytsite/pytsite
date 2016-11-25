"""PytSite Theme API.
"""
import json as _json
from typing import Dict as _Dict
from importlib.util import find_spec as _find_module_spec
from os import path as _path
from pytsite import threading as _threading, logger as _logger, reg as _reg
from . import _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_themes_path = _path.join(_reg.get('paths.root'), 'themes')

# Available themes
_themes = {}  # type: _Dict[str, _Dict]

# Thread safe current theme
_current = {}  # type: _Dict[int, str]


def get_themes_path():
    """Get absolute path of themes location.
    """
    return _themes_path


def register(package_name: str):
    """Register a theme.
    """
    if package_name in _themes:
        raise RuntimeError("Theme '{}' is already registered".format(package_name))

    # Check for package existence
    spec = _find_module_spec(package_name)
    if not spec:
        raise _error.ThemeRegistrationFailed("Theme package '{}' is not found".format(package_name))

    # Build paths
    theme_path = _path.dirname(spec.origin)
    info_path = _path.join(theme_path, 'theme.json')

    # Load info file
    try:
        with open(info_path) as f:
            info_data = _json.load(f)  # type: dict
    except FileNotFoundError:
        raise _error.ThemeRegistrationFailed('Theme info file is not found at {}'.format(info_path))
    except _json.JSONDecodeError as e:
        raise _error.ThemeRegistrationFailed('Error while loading {}: {}'.format(info_path, e))

    # Check data
    if not isinstance(info_data, dict):
        raise _error.ThemeRegistrationFailed('Dictionary expected in {}'.format(info_path))

    # Extract data
    theme_name = info_data.get('name')
    theme_desc = info_data.get('description')
    theme_author = info_data.get('author')
    theme_url = info_data.get('url')

    # Check data
    if not theme_name:
        raise _error.ThemeRegistrationFailed('Theme name is not specified in {}'.format(info_path))

    # Register resources
    if _path.exists(_path.join(theme_path, 'lang')):
        from pytsite import lang
        lang.register_package(package_name, 'lang')
    if _path.exists(_path.join(theme_path, 'tpl')):
        from pytsite import tpl
        tpl.register_package(package_name, 'tpl')
    if _path.exists(_path.join(theme_path, 'assets')):
        from pytsite import assetman
        assetman.register_package(package_name, 'assets')

    _themes[package_name] = {
        'name': theme_name,
        'description': theme_desc,
        'author': theme_author,
        'url': theme_url,
    }

    if len(_themes) == 1:
        set_current(package_name)

    # Start theme
    __import__(package_name)

    _logger.info("Theme '{}' successfully loaded from '{}'".format(theme_name, package_name))


def get_list() -> _Dict[str, _Dict]:
    """Get available themes.
    """
    return _themes.copy()


def get_info(package_name: str) -> dict:
    """Get information about theme.
    """
    if package_name not in _themes:
        raise _error.ThemeNotRegistered("Theme '{}' is not registered".format(package_name))

    return _themes[package_name].copy()


def is_registered(package_name: str) -> bool:
    """Check if theme is registered.
    """
    return package_name in _themes


def set_current(package_name: str):
    """Set current theme.
    """
    if package_name not in _themes:
        raise RuntimeError("Theme '{}' is not registered".format(package_name))

    _current[_threading.get_id()] = package_name


def get_current() -> str:
    """Get current theme.
    """
    if not _themes:
        raise _error.NoThemesRegistered('No registered themes found')

    tid = _threading.get_id()
    return _current[tid] if tid in _current else list(_themes.keys())[0]
