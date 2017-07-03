"""PytSite Theme
"""
from importlib import import_module as _import_module
from os import path as _path, makedirs as _makedirs
from pytsite import settings as _settings, logger as _logger, pkg_util as _pkg_util, util as _util
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
        # Check requirements
        _pkg_util.check_requirements(package_name, 'theme.json')

        # Load package data from JSON file
        pkg_data = _pkg_util.parse_json(package_name, 'theme.json')

        # Check data
        for k in ('name', 'description', 'version'):
            if k not in pkg_data or not pkg_data[k]:
                raise _error.ThemeInitError("'{}' is not found or empty in theme's JSON".format(k))

        self._package_name = package_name
        self._path = _pkg_util.resolve_path(package_name)
        self._name = _util.transform_str_2(pkg_data.get('name'))
        self._version = pkg_data.get('version')
        self._description = pkg_data.get('description')
        self._author = pkg_data.get('author')
        self._url = pkg_data.get('url')

        self._package = None  # Will be filled after loading
        self._is_loaded = False

    def load(self):
        """Load the theme
        """
        from pytsite import lang, tpl, assetman

        # Register translations package
        lang_path = _path.join(self._path, 'lang')
        if not _path.exists(lang_path):
            _makedirs(lang_path, 0o755, True)
        lang.register_package(self._package_name, 'lang')

        # Register templates package
        tpl_path = _path.join(self._path, 'tpl')
        if not _path.exists(tpl_path):
            _makedirs(tpl_path, 0o755, True)
        tpl.register_package(self._package_name, 'tpl')

        # Register assetman package
        assets_path = _path.join(self._path, 'assets')
        if not _path.exists(assets_path):
            _makedirs(assets_path, 0o755, True)
        assetman.register_package(self._package_name, 'assets')

        # Load theme module
        try:
            self._package = _import_module(self._package_name)
            _logger.info("Theme '{}' successfully loaded from '{}'".format(self._package_name, self._path))
        except ImportError as e:
            raise _error.ThemeLoadError("Error while loading theme package '{}': {}".format(self._package_name, e))

        # Compile assets
        if not _settings.get('theme.compiled'):
            try:
                assetman.build(self._package_name)
                _settings.put('theme.compiled', True)
            except assetman.error.NoTasksDefined as e:
                _logger.warn(e)

        self._is_loaded = True

        return self

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
    def version(self) -> str:
        return self._version

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
