"""PytSite Theme
"""
import re as _re
import json as _json
from importlib import import_module as _import_module
from importlib.util import find_spec as _find_module_spec
from os import path as _path, mkdir as _mkdir
from pytsite import reg as _reg, logger as _logger, settings as _settings
from . import _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Theme:
    """PytSite Theme
    """

    def __init__(self, package_name: str):
        """Init
        """
        # Check for package existence
        spec = _find_module_spec(package_name)
        if not spec or not spec.loader:
            raise _error.ThemeRegistrationFailed("Theme package '{}' doesn't exist or it is not a package".
                                                 format(package_name))

        # Build paths
        theme_path = _path.dirname(_path.join(_reg.get('paths.root'), spec.origin))
        theme_path = theme_path.replace('{}.{}'.format(_path.sep, _path.sep), _path.sep)
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

        self._package_name = package_name
        self._path = theme_path
        self._name = _re.sub('\W', '_', package_name[package_name.rfind('.') + 1:].lower())
        self._description = info_data.get('description')
        self._author = info_data.get('author')
        self._url = info_data.get('url')
        self._package = None  # Will be filled after loading
        self._is_loaded = False

    def load(self):
        """Load theme
        """
        if self._is_loaded:
            raise _error.ThemeAlreadyLoaded('Theme is already loaded')

        # Create directories for resources
        for n in 'lang', 'tpl', 'assets':
            n_path = _path.join(self._path, n)
            if not _path.exists(n_path):
                _mkdir(n_path, 0o755)

        # Register resources
        from pytsite import lang, tpl, assetman
        lang.register_package(self._package_name, 'lang')
        tpl.register_package(self._package_name, 'tpl')
        assetman.register_package(self._package_name, 'assets')

        try:
            self._package = _import_module(self._package_name)
        except ImportError as e:
            raise _error.ThemeRegistrationFailed("Error while loading theme package '{}': {}".
                                                 format(self._package_name, e))

        self._is_loaded = True
        _logger.info("Theme '{}' successfully loaded from '{}'".format(self._name, self._package_name))

    @property
    def package_name(self) -> str:
        return self._package_name

    @property
    def path(self) -> str:
        return self._path

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def author(self) -> str:
        return self._author

    @property
    def url(self) -> str:
        return self._url

    @property
    def package(self):
        return self._package

    @property
    def is_loaded(self) -> bool:
        return self._is_loaded

    @property
    def settings(self) -> dict:
        return _settings.get('theme.theme_' + self._name, {})
