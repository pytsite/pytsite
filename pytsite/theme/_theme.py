"""PytSite Theme
"""
import json as _json
from importlib.util import find_spec as _find_module_spec
from os import path as _path
from pytsite import reg as _reg, settings as _settings
from . import _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Theme:
    """PytSite Theme
    """

    def __init__(self, name: str):
        """Init
        """
        # Check for package existence
        spec = _find_module_spec(name)
        if not spec or not spec.loader:
            raise _error.ThemeInitError("Theme package '{}' doesn't exist or it is not a package".
                                        format(name))

        # Build paths
        theme_path = _path.dirname(_path.join(_reg.get('paths.root'), spec.origin))
        theme_path = theme_path.replace('{}.{}'.format(_path.sep, _path.sep), _path.sep)
        info_path = _path.join(theme_path, 'theme.json')

        # Load info file
        try:
            with open(info_path) as f:
                info_data = _json.load(f)  # type: dict
        except FileNotFoundError:
            raise _error.ThemeInitError('Theme info file is not found at {}'.format(info_path))
        except _json.JSONDecodeError as e:
            raise _error.ThemeInitError('Error while loading {}: {}'.format(info_path, e))

        # Check data
        if not isinstance(info_data, dict):
            raise _error.ThemeInitError('Dictionary expected in {}'.format(info_path))

        self._name = name
        self._path = theme_path
        self._description = info_data.get('description')
        self._author = info_data.get('author')
        self._url = info_data.get('url')
        self._package = None  # Will be filled after loading
        self._is_loaded = False

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
