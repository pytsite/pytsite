"""PytSite Package Manager API Functions.
"""
import zipfile as _zipfile
import json as _json
import pip as _pip
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
_started = []
_installing = []
_uninstalling = []

_plugins_path = _path.join(_reg.get('paths.root'), 'plugins')
_plugins_package_name = 'plugins'
_plugins_path_dev = _path.join(_reg.get('paths.root'), 'plugins-dev')
_plugins_package_name_dev = 'plugins-dev'


def _get_plugin_path(plugin_name: str) -> str:
    """Calculate local path of a plugin.
    """
    return _path.join(_plugins_path, plugin_name)


def _get_plugin_info_path(plugin_name: str) -> str:
    """Calculate local path of a plugin's info file.
    """
    return _path.join(_get_plugin_path(plugin_name), 'plugin.json')


def _get_local_info(plugin_name: str) -> dict:
    """Get information about locally installed plugin.
    """
    if not is_installed(plugin_name):
        raise _error.PluginNotInstalled("Plugin '{}' is not installed".format(plugin_name))

    plugin_info_path = _get_plugin_info_path(plugin_name)
    data = {}

    if not _path.exists(plugin_info_path):
        # Create the info file if it doest not exist
        with open(plugin_info_path, 'wt') as f:
            f.write('{}\n')
    else:
        # Load data from the info file
        with open(plugin_info_path) as f:
            data = _json.load(f)  # type: dict

        if not isinstance(data, dict):
            raise TypeError('{} should contain dictionary, got {}'.format(plugin_info_path, type(data)))

    return data


def _write_local_info(plugin_name: str, data: dict):
    """Update plugin's info file.
    """
    if not is_installed(plugin_name):
        raise _error.PluginNotInstalled("Plugin '{}' is not installed".format(plugin_name))

    with open(_get_plugin_info_path(plugin_name), 'wt') as f:
        _json.dump(data, f)


def _get_remote_info() -> dict:
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
            'latest_version': latest_version,
            'latest_version_url': versions[latest_version],
        }

    return _plugins_cache.put('github', r, 3600)  # GitHub allows only 60 requests per hour


def get_plugins_path() -> str:
    """Get plugins local directory location.
    """
    return _plugins_path


def is_installed(plugin_name: str) -> bool:
    """Check if the plugin is installed.
    """
    return _path.isdir(_get_plugin_path(plugin_name))


def is_started(plugin_name: str) -> bool:
    """Check if the plugin is started.
    """
    return plugin_name in _started


def start(plugin_name: str, dev: bool=False) -> object:
    """Start a plugin.
    """
    if not dev and not is_installed(plugin_name):
        raise _error.PluginNotInstalled("Plugin '{}' is not installed".format(plugin_name))

    if plugin_name in _started:
        raise _error.PluginStartError("Plugin '{}' is already started.".format(plugin_name))

    pkg_name = (_plugins_package_name_dev if dev else _plugins_package_name) + '.' + plugin_name

    try:

        module = _import_module(pkg_name)
        _started.append(plugin_name)
        _logger.info("Plugin '{}' ({}) successfully started".format(plugin_name, pkg_name))

        return module

    except Exception as e:
        raise _error.PluginStartError("Error while starting plugin '{}' ({}): {}".format(plugin_name, pkg_name, e))


def get_info(plugin_name: str = None) -> dict:
    """Get combined information about remotely available and locally installed plugin(s).
    """
    required = _reg.get('plugins', ())

    # Fetch data about existing plugins from GitHub
    r = _get_remote_info()

    # Add
    for name, info in r.items():
        local_info = _get_local_info(name) if is_installed(name) else {}
        installed_version = local_info.get('version')

        r[name].update({
            'installed_version': installed_version,
            'installing': name in _installing,
            'uninstalling': name in _uninstalling,
            'upgradable': bool(installed_version and r[name]['latest_version'] != installed_version),
            'required': name in required,
            'requires': local_info.get('requires', ()),
        })

    if plugin_name:
        try:
            return r[plugin_name]
        except KeyError:
            raise _error.UnknownPlugin("Plugin '{}' does not exist.".format(plugin_name))
    else:
        return r


def get_info_dev(plugin_name: str = None) -> dict:
    """Get information about plugin in development.
    """
    r = {}

    if not _path.exists(_plugins_path_dev):
        return r

    for item in _listdir(_plugins_path_dev):
        abs_path = _path.join(_plugins_path_dev, item)
        if not _path.isdir(abs_path):
            continue

        r[item] = {
            'path': abs_path,
        }

    if plugin_name:
        try:
            r = r[plugin_name]
        except KeyError:
            raise _error.UnknownPlugin("Development plugin '{}' does not exist.".format(plugin_name))

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
        version = plugin_info['latest_version']
        zip_url = plugin_info['latest_version_url']
        home_url = plugin_info['home_url']
        tmp_file_path = _path.join(tmp_dir_path, '{}-{}.zip'.format(plugin_name, version))

        # Download archive
        _logger.info('Downloading {} to {}'.format(zip_url, tmp_file_path))
        _urlretrieve(zip_url, tmp_file_path)
        _logger.info('{} successfully stored to {}'.format(zip_url, tmp_file_path))

        # Extract downloaded archive
        _logger.info('Extracting {} into {}'.format(tmp_file_path, tmp_dir_path))
        with _zipfile.ZipFile(tmp_file_path) as z_file:
            z_file.extractall(tmp_dir_path)
        _logger.info('{} successfully extracted to {}'.format(tmp_file_path, tmp_dir_path))

        # Remove downloaded archive
        _unlink(tmp_file_path)
        _logger.info('{} removed'.format(tmp_file_path))

        # Move extracted directory to the plugins directory
        extracted_dir_prefix = '{}-{}{}'.format(_GITHUB_REPO, _GITHUB_PLUGIN_REPO_PREFIX, plugin_name)
        for dir_name in _listdir(tmp_dir_path):
            if not dir_name.startswith(extracted_dir_prefix):
                continue

            source_dir_path = _path.join(tmp_dir_path, dir_name)
            target_dir_path = _get_plugin_path(plugin_name)

            _rename(source_dir_path, target_dir_path)
            _logger.info('{} moved to {}'.format(source_dir_path, target_dir_path))

            # Update info file
            local_info = _get_local_info(plugin_name)
            local_info.update({
                'name': plugin_name,
                'description': description,
                'version': version,
                'home_url': home_url,
                'zip_url': zip_url,
                'installed': _util.w3c_datetime_str(),
            })

            _write_local_info(plugin_name, local_info)

    finally:
        _installing.remove(plugin_name)

    # Load info after plugin installation
    info = get_info(plugin_name)

    # Install required packages
    if 'packages' in info['requires'] and info['requires']['packages']:
        for pkg_name in info['requires']['packages']:
            _logger.info('Installing required package: {}'.format(pkg_name))
            r = _pip.main(['install', pkg_name, '-qqq'])
            if r != 0:
                _logger.warn('There were errors while installing package {}'.format(pkg_name))
            _logger.info('Required package {} has been successfully installed'.format(pkg_name))

    # Install required plugins
    if 'plugins' in info['requires'] and info['requires']['plugins']:
        for plg_name in info['requires']['plugins']:
            _logger.info('Installing required plugin: {}'.format(plg_name))
            install(plg_name)

    # Application should be reloaded to activate installed plugin
    _reload.set_flag()


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
