"""PytSite Package Manager API Functions.
"""
import sys as _sys
import zipfile as _zipfile
import json as _json
from os import listdir as _listdir, path as _path, mkdir as _mkdir, unlink as _unlink, rename as _rename
from shutil import rmtree as _rmtree
from importlib import import_module as _import_module
from urllib.request import urlretrieve as _urlretrieve
from pytsite import reg as _reg, github as _github, semver as _semver, logger as _logger, util as _util, \
    cache as _cache, reload as _reload
from . import _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_GITHUB_REPO = 'pytsite'
_GITHUB_PLUGIN_REPO_PREFIX = 'plugin-'

_plugins_cache = _cache.create_pool('pytsite.plugman')
_installing = []
_uninstalling = []


def _get_plugin_path(plugin_name: str) -> str:
    """Calculate local path of a plugin.
    """
    return _path.join(_reg.get('paths.plugins'), plugin_name)


def _get_local_info(plugin_name: str) -> dict:
    """Get information about locally installed plugin.
    """
    if not is_installed(plugin_name):
        raise _error.PluginNotInstalled("Plugin '{}' is not installed".format(plugin_name))

    # Check if the info file exists
    info_file_path = _path.join(_get_plugin_path(plugin_name), 'plugman.json')
    if not _path.exists(info_file_path):
        raise _error.UnknownPlugin("File {} is not found".format(info_file_path))

    # Load data from info file
    with open(info_file_path) as f:
        data = _json.load(f)

    return data


def _update_local_info(plugin_name: str, key: str, value) -> dict:
    """Get information about locally installed plugin.
    """
    data = _get_local_info(plugin_name)

    data[key] = value

    with open(_path.join(_get_plugin_path(plugin_name), 'plugman.json'), 'w') as f:
        _json.dump(data, f)

    return data


def _get_github_data() -> dict:
    """Load data about available plugins from GitHub.
    """
    if _plugins_cache.has('github'):
        return _plugins_cache.get('github')

    r = {}

    gh = _github.Session()

    for repo in gh.org_repos(_GITHUB_REPO):
        if not repo['name'].startswith(_GITHUB_PLUGIN_REPO_PREFIX):
            continue

        name = repo['name'].replace(_GITHUB_PLUGIN_REPO_PREFIX, '')

        # Load versions from repo's tags
        versions = {v['name']: v['zipball_url'] for v in gh.repo_tags(repo['owner']['login'], repo['name'])}
        if not versions:
            continue

        latest_version = _semver.latest(versions.keys())

        r[name] = {
            'name': name,
            'home_url': repo['html_url'],
            'description': repo['description'],
            'latest_version': (latest_version, versions[latest_version]),
        }

    return _plugins_cache.put('github', r, 3600)  # GitHub allows only 60 requests per hour


def start(plugin_name: str) -> object:
    """Start a plugin.
    """
    if not is_installed(plugin_name):
        raise _error.PluginNotInstalled("Plugin '{}' is not installed".format(plugin_name))

    if 'app.plugins.' + plugin_name in _sys.modules:
        raise _error.PluginStartError("Plugin '{}' is already started.".format(plugin_name))

    try:
        module = _import_module('app.plugins.' + plugin_name)

        _logger.info("Plugin '{}' successfully started".format(plugin_name))

        return module

    except Exception as e:
        raise _error.PluginStartError("Error while starting plugin '{}': {}".format(plugin_name, e))


def is_installed(plugin_name: str) -> bool:
    """Check if the plugin is installed.
    """
    return _path.isdir(_get_plugin_path(plugin_name))


def get_info(plugin_name: str = None) -> dict:
    """Get information about plugin(s).
    """
    # Fetch data about existing plugins from GitHub
    r = _get_github_data()

    # Add
    for name, info in r.items():
        installed_version = _get_local_info(name)['version'] if is_installed(name) else None

        r[name].update({
            'installed_version': installed_version,
            'installing': name in _installing,
            'uninstalling': name in _uninstalling,
            'upgradable': bool(installed_version and r[name]['latest_version'][0] != installed_version),
        })

    if plugin_name:
        try:
            return r[plugin_name]
        except KeyError:
            raise _error.UnknownPlugin("Plugin '{}' does not exist.".format(plugin_name))
    else:
        return r


def install(plugin_name: str) -> dict:
    """Install latest version of a plugin.
    """
    global _installing

    # Check if the plugin is not installing at this moment
    if plugin_name in _installing:
        raise _error.PluginInstallationInProgress(
            "Installation of the plugin '{}' already started".format(plugin_name))

    # Check if the plugin is already installed
    if is_installed(plugin_name):
        raise _error.PluginAlreadyInstalled("Plugin '{}' is already installed".format(plugin_name))

    try:
        # Flag start of the installation process
        _installing.append(plugin_name)

        # Create temporary directory to store plugin's content
        tmp_dir_path = _path.join(_reg.get('paths.tmp'), 'plugman')
        if not _path.exists(tmp_dir_path):
            _mkdir(tmp_dir_path, 0o755)

        # Prepare all necessary data
        plugin_info = get_info(plugin_name)
        description = plugin_info['description']
        version = plugin_info['latest_version'][0]
        zip_url = plugin_info['latest_version'][1]
        home_url = plugin_info['home_url']
        tmp_file_path = _path.join(tmp_dir_path, '{}-{}.zip'.format(plugin_name, version))

        # Download remote ZIP
        _logger.info('Downloading {} to {}'.format(zip_url, tmp_file_path))
        _urlretrieve(zip_url, tmp_file_path)
        _logger.info('{} successfully stored to {}'.format(zip_url, tmp_file_path))

        # Extract ZIP
        _logger.info('Extracting {} into {}'.format(tmp_file_path, tmp_dir_path))
        with _zipfile.ZipFile(tmp_file_path) as z_file:
            z_file.extractall(tmp_dir_path)
        _logger.info('{} successfully extracted to {}'.format(tmp_file_path, tmp_dir_path))

        # Remove ZIP
        _unlink(tmp_file_path)
        _logger.info('{} removed'.format(tmp_file_path))

        # Move extracted directory to the plugins directory
        extracted_dir_prefix = '{}-{}{}'.format(_GITHUB_REPO, _GITHUB_PLUGIN_REPO_PREFIX, plugin_name)
        for dir_name in _listdir(tmp_dir_path):
            if not dir_name.startswith(extracted_dir_prefix):
                continue

            source_dir_path = _path.join(tmp_dir_path, dir_name)
            target_dir_path = _path.join(_reg.get('paths.plugins'), plugin_name)

            _rename(source_dir_path, target_dir_path)
            _logger.info('{} moved to {}'.format(source_dir_path, target_dir_path))

            # Create info file
            with open(_path.join(target_dir_path, 'plugman.json'), 'w') as f:
                data = {
                    'name': plugin_name,
                    'description': description,
                    'version': version,
                    'home_url': home_url,
                    'zip_url': zip_url,
                    'installed': _util.w3c_datetime_str(),
                }

                _json.dump(data, f)

            # Application should be reloaded to activate installed plugin
            _reload.set_flag()

            return data

    finally:
        _installing.remove(plugin_name)


def uninstall(plugin_name: str):
    """Uninstall a plugin.
    """
    # Check if the plugin is not installing at this moment
    if plugin_name in _uninstalling:
        raise _error.PluginUninstallationInProgress(
            "Uninstallation of the plugin '{}' is already started".format(plugin_name))

    if not is_installed(plugin_name):
        raise _error.PluginNotInstalled("Plugin '{}' is not installed".format(plugin_name))

    try:
        _uninstalling.append(plugin_name)

        # Delete plugin's files
        _rmtree(_get_plugin_path(plugin_name))

        _logger.info("Plugin '{}' successfully uninstalled".format(plugin_name))

        # Application should be reloaded to deactivate installed plugin
        _reload.set_flag()

    finally:
        _uninstalling.remove(plugin_name)


def upgrade(plugin_name: str) -> dict:
    """Upgrade a locally installed plugin.
    """
    if not is_installed(plugin_name):
        raise _error.PluginNotInstalled("Plugin '{}' is not installed".format(plugin_name))

    # Uninstall
    uninstall(plugin_name)

    # Install
    data = install(plugin_name)

    return data
