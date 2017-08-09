"""PytSite Theme API Functions
"""
from typing import Dict as _Dict
from os import path as _path, unlink as _unlink, chdir as _chdir, getcwd as _getcwd, rmdir as _rmdir
from shutil import rmtree as _rmtree, move as _move
from zipfile import ZipFile as _ZipFile
from glob import glob as _glob
from pytsite import reg as _reg, settings as _settings, logger as _logger, reload as _reload, util as _util
from . import _theme, _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_themes_path = _path.join(_reg.get('paths.root'), 'themes')

# All registered themes
_themes = {}  # type: _Dict[str, _theme.Theme]

# First registered theme
_fallback = None  # type: _theme.Theme

# Currently loaded theme
_loaded = None  # type: _theme.Theme


def _extract_archive(src_file_path: str, dst_dir_path):
    """Extract theme archive
    """

    # Extract all files
    with _ZipFile(src_file_path) as z_file:
        z_file.extractall(dst_dir_path)

    # Check if the archive contents only single directory, move its files up
    orig_cwd = _getcwd()
    _chdir(dst_dir_path)
    files_list = _glob('*')
    if len(files_list) == 1 and _path.isdir(files_list[0]):
        top_directory = files_list[0]
        _chdir(top_directory)

        f_names = _glob('*') + _glob('.*')
        for f_name in f_names:
            if f_name not in ('.', '..'):
                _move(f_name, dst_dir_path)

        _chdir('..')
        _rmdir(top_directory)

    _chdir(orig_cwd)

    _logger.info("Theme files successfully extracted from file '{}' to directory '{}'".
                 format(src_file_path, dst_dir_path))


def themes_path():
    """Get absolute filesystem path to themes location
    """
    return _themes_path


def get(package_name: str = None) -> _theme.Theme:
    """Get theme by package name or default
    """
    if not _themes:
        raise _error.NoThemesRegistered()

    if not package_name:
        return _loaded or _fallback

    try:
        return _themes[package_name]
    except KeyError:
        raise _error.ThemeNotRegistered(package_name)


def switch(package_name: str):
    """Switch current theme
    """
    if package_name not in _themes:
        raise _error.ThemeNotRegistered(package_name)

    # Switch only if it really necessary
    if package_name != get().package_name:
        _settings.put('theme.current', package_name)  # Mark theme as current
        _settings.put('theme.compiled', False)  # Mark that assets compilation needed
        _reload.reload(0.1)


def register(package_name: str):
    """Register a theme
    """
    global _fallback

    if package_name in _themes:
        raise _error.ThemeAlreadyRegistered(package_name)

    theme = _theme.Theme(package_name)

    if not _fallback or theme.package_name == _settings.get('theme.current'):
        _fallback = theme

    _themes[package_name] = theme


def get_registered() -> _Dict[str, _theme.Theme]:
    """Get all registered themes
    """
    return _themes


def load(package_name: str = None) -> _theme.Theme:
    """Load theme
    """
    global _loaded

    # Only one theme can be loaded
    if _loaded:
        raise _error.ThemeLoadError("Cannot load theme '{}', because another theme '{}' is already loaded".
                                    format(package_name, _loaded.package_name))

    # Load theme
    _loaded = get(package_name).load()

    return _loaded


def install(archive_path: str, delete_zip_file: bool = True):
    """Install a theme from a zip-file
    """
    _logger.info('Requested theme installation from zip-file {}'.format(archive_path))

    # Create temporary directgory
    tmp_dir_path = _util.mk_tmp_dir(subdir='theme')

    try:
        # Extract archove to the temporary directory
        _extract_archive(archive_path, tmp_dir_path)

        # Try to initialize the theme to ensure everything is okay
        theme = _theme.Theme('tmp.theme.{}'.format(_path.basename(tmp_dir_path)))

        # Theme has been successfully initialized, so now it can be moved to the 'themes' package
        dst_path = _path.join(_themes_path, theme.name)
        if _path.exists(dst_path):
            _logger.info("Existing theme installation at '{}' will be replaced with new one".format(dst_path))
            _rmtree(dst_path)

        # Move directory to the final location
        _move(tmp_dir_path, dst_path)
        _logger.info("'{}' has been successfully installed to '{}'".format(tmp_dir_path, dst_path))

        _reload.reload(0.1)

    except Exception as e:
        _logger.error(e, exc_info=True)
        raise e

    finally:
        if _path.exists(tmp_dir_path):
            _rmtree(tmp_dir_path)

        if delete_zip_file:
            _unlink(archive_path)


def uninstall(package_name: str):
    theme = get(package_name)

    if theme.name == get().name:
        raise RuntimeError('Cannot uninstall current theme, please switch to another theme before doing uninstallation')

    del _themes[package_name]
    _rmtree(theme.path)

    _logger.info("Theme '{}' has been successfully uninstalled from '{}'".format(theme.name, theme.path))
