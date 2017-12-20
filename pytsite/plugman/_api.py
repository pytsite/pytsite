"""PytSite Package Manager API
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import zipfile as _zipfile
import requests as _requests
import json as _json
from typing import Union as _Union, Dict as _Dict
from os import listdir as _listdir, path as _path, mkdir as _mkdir, unlink as _unlink, rename as _rename
from shutil import rmtree as _rmtree
from importlib import import_module as _import_module, reload as _reload_module
from urllib.request import urlretrieve as _urlretrieve
from datetime import datetime as _datetime
from pytsite import reg as _reg, logger as _logger, lang as _lang, util as _util, router as _router, \
    console as _console, semver as _semver, package_info as _package_info, cache as _cache, reload as _reload, \
    events as _events
from . import _error

_PLUGINS_API_URL = _reg.get('plugman.api_url', 'https://plugins.pytsite.xyz')
_DEV_MODE = _router.server_name() == 'local.plugins.pytsite.xyz'

_GITHUB_ORG = 'pytsite'
_GITHUB_PLUGIN_REPO_PREFIX = 'plugin-'
_DEBUG = _reg.get('plugman.debug', False)

_loading = {}  # type: _Dict[str, str]
_loaded = {}  # type: _Dict[str, str]
_installing = []
_uninstalling = []
_required = set(_reg.get('plugman.plugins', []))
_plugman_cache = _cache.create_pool('pytsite.plugman')

_PLUGINS_PATH = _path.join(_reg.get('paths.root'), 'plugins')
_PLUGINS_PACKAGE_NAME = 'plugins'

_reg.put('paths.plugins', _PLUGINS_PATH)


def _plugin_path(plugin_name: str) -> str:
    """Calculate local path of a plugin
    """
    if plugin_name.startswith('plugins.'):
        plugin_name = plugin_name[8:]

    return _path.join(_PLUGINS_PATH, plugin_name)


def plugins_path() -> str:
    """Get plugins local directory location
    """
    return _PLUGINS_PATH


def _plugins_api_request(endpoint: str, args: dict = None) -> dict:
    """Do a request to plugins API host
    """
    request_url = _PLUGINS_API_URL + '/api/2/' + endpoint

    if args is None:
        args = {}

    args.update({
        'h': _router.server_name(),
    })

    r = _requests.get(request_url, args)

    if not r.ok:
        try:
            raise _error.PluginsApiError(request_url, r.json().get('error'))
        except _json.JSONDecodeError:
            raise _error.PluginsApiError(request_url, 'Error while parsing JSON from string: {}'.format(r.content))

    return r.json()


def _install_pip_package(pkg_spec: str, upg: bool = False):
    """Install a pip package
    """
    _console.print_info('Installing/upgrading pip package: {}'.format(pkg_spec))

    _util.install_pip_package(pkg_spec, upg)

    _console.print_success('Required pip package {} has been successfully installed'.format(pkg_spec))


def plugin_package_info(plugin_name: str) -> dict:
    """Get information about local plugin
    """
    try:
        plugin_pkg_name = 'plugins.{}'.format(plugin_name)

        return _package_info.data(plugin_pkg_name, defaults={
            'name': plugin_pkg_name,
            'version': '0.0.1',
        })

    except _package_info.error.PackageNotFound:
        raise _error.PluginPackageNotFound(plugin_name)


def is_installed(plugin_spec: _Union[str, list, tuple]) -> bool:
    """Check if the plugin is installed
    """
    if isinstance(plugin_spec, (list, tuple)):
        for p_spec in plugin_spec:
            if not is_installed(p_spec):
                return False

        return True

    if plugin_spec.startswith('plugins.'):
        plugin_spec = plugin_spec[8:]

    plugin_name, version_req = _semver.parse_requirement_str(plugin_spec)

    # Check if the plugin exists on the filesystem
    if _DEV_MODE:
        if not _path.exists(_plugin_path(plugin_name)):
            return False
    else:
        if not _path.exists(_path.join(_plugin_path(plugin_name), 'installed')):
            return False

    # Check plugin version
    return _semver.check_conditions(_package_info.version('plugins.' + plugin_name), version_req)


def is_loaded(plugin_name: str) -> bool:
    """Check if the plugin is loaded
    """
    return plugin_name in _loaded


def load(plugin_spec: _Union[str, list, tuple], _required_by_spec: str = None) -> object:
    """Load a plugin
    """
    global _required, _loaded, _loading, _installing

    # Multiple load requested
    if isinstance(plugin_spec, (list, tuple)):
        for p_spec in plugin_spec:
            load(p_spec)

    # Normalize plugin spec
    plugin_name, version_req = _semver.parse_requirement_str(plugin_spec)
    plugin_spec = '{}{}'.format(plugin_name, version_req)

    # Check if the plugin installed
    if not is_installed(plugin_spec):
        raise _error.PluginNotInstalled(plugin_spec, _required_by_spec)

    # Check if the plugin is already loaded
    if plugin_name in _loaded:
        if _DEBUG:
            _logger.debug("Plugin '{}' already loaded".format(_loaded[plugin_name]))
        return

    # Checking for circular dependency
    if plugin_name in _loading:
        raise _error.CircularDependencyError(plugin_name, _loading[plugin_name])

    # Mark plugin as loading
    _loading[plugin_name] = _required_by_spec

    # Get info about plugin, but NOT actually load it
    try:
        p_info = plugin_package_info(plugin_name)
    except _error.PluginPackageNotFound as e:
        _console.print_warning(str(e))
        return

    # Load required plugins
    for req_plugin_spec_str in p_info['requires']['plugins']:
        req_plugin_spec = _semver.parse_requirement_str(req_plugin_spec_str)
        _required.add(req_plugin_spec[0])
        if _DEBUG:
            _logger.debug("Plugin '{}-{}' requires '{}{}'".format(plugin_name, p_info['version'],
                                                                  req_plugin_spec[0], req_plugin_spec[1]))
        load(req_plugin_spec_str, '{}-{}'.format(plugin_name, p_info['version']))

    try:
        plugin_module_name = _PLUGINS_PACKAGE_NAME + '.' + plugin_name

        # Import plugin's package
        mod = _import_module(plugin_module_name)

        # plugin_load() hook
        if hasattr(mod, 'plugin_load') and callable(mod.plugin_load):
            mod.plugin_load()

        # plugin_load_{env.type}() hook
        env_hook = 'plugin_load_{}'.format(_reg.get('env.type'))
        if hasattr(mod, env_hook):
            getattr(mod, env_hook)()

        _loaded[plugin_name] = '{}-{}'.format(plugin_name, p_info['version'])
        if _DEBUG:
            _logger.debug("Plugin '{}-{}' loaded".format(plugin_name, p_info['version']))
        del _loading[plugin_name]

        return mod

    except Exception as e:
        raise _error.PluginLoadError("Error while loading plugin '{}-{}': {}".
                                     format(plugin_name, p_info['version'], e))


def plugins_info() -> dict:
    """Get information about all installed plugins
    """
    r = {}
    for plugin_name in _listdir(_PLUGINS_PATH):
        plugin_path = _path.join(_PLUGINS_PATH, plugin_name)
        if _path.isdir(plugin_path) and not (plugin_name.startswith('.') or plugin_name.startswith('_')):
            r[plugin_name] = plugin_package_info(plugin_name)

    return r


def remote_plugin_info(plugin_name: str, versions_spec: list = None):
    """Get information about remote plugin
    """
    versions = ','.join(versions_spec) if versions_spec else '>0.0.0'

    return _plugins_api_request('plugin/{}'.format(plugin_name), {'version': versions})


def remote_plugins_info() -> dict:
    """Get information about available remote plugins
    """
    try:
        return _plugman_cache.get('remote_plugins')
    except _cache.error.KeyNotExist:
        return _plugman_cache.put('remote_plugins', _plugins_api_request('plugins'), 900)  # 15 min TTL


def get_dependant_plugins(plugin_name: str) -> list:
    """Get locally installed plugin names which are dependant from plugin_name
    """
    if not is_installed(plugin_name):
        raise _error.PluginNotInstalled(plugin_name)

    r = []
    for p_name, p_info in plugins_info().items():
        if p_name != plugin_name and plugin_name in p_info['requires']['plugins']:
            r.append(p_name)

    return r


def get_allowed_version_range(plugin_name: str) -> dict:
    """Calculate minimum and maximum allowed plugin version for local installation
    """
    r = {'min': '0.0.0', 'max': '99.99.99'}

    # Build list of packages to collect information from
    pkg_names = ['app']
    for installed_plugin_name in plugins_info():
        if installed_plugin_name != plugin_name:
            pkg_names.append('plugins.{}'.format(installed_plugin_name))

    # Ask each package for its requirements
    for pkg_name in pkg_names:
        for required_plugin_spec in _package_info.requires_plugins(pkg_name):
            required_plugin_name, required_plugin_ver = _semver.parse_requirement_str(required_plugin_spec)
            if required_plugin_name != plugin_name:
                continue

            min_ver = _semver.minimum(required_plugin_ver)
            max_ver = _semver.maximum(required_plugin_ver)

            if _semver.compare(r['min'], min_ver) < 0:
                r['min'] = min_ver
            if _semver.compare(r['max'], max_ver) > 0:
                r['max'] = max_ver

    return r


def install(plugin_spec: str) -> int:
    """Install a plugin

    Returns a number of installed plugins, including dependencies
    """
    global _installing
    installed_count = 0

    if _DEV_MODE:
        raise RuntimeError(_lang.t('pytsite.plugman@cannot_manage_plugins_in_dev_mode'))

    # Extract plugin name and desired version
    plugin_name, desired_v_spec = _semver.parse_requirement_str(plugin_spec)
    desired_v_op = _semver.parse_condition_str(desired_v_spec)[0]

    # Get version constraints from other plugins, current theme and application
    allowed_versions = get_allowed_version_range(plugin_name)
    allowed_v_min = allowed_versions['min']
    allowed_v_max = allowed_versions['max']

    # Get desired minimal and maximal versions
    desired_v_min = _semver.minimum(desired_v_spec)
    desired_v_max = _semver.maximum(desired_v_spec)

    # If desired version is lower than allowed
    if _semver.compare(desired_v_min, allowed_v_min) < 0:
        if desired_v_op != '==':
            desired_v_min = allowed_v_min
        else:
            raise _error.PluginDependencyError('{}{} cannot be installed because acceptable version is {}'
                                               .format(plugin_name, desired_v_spec, allowed_versions))
    # If desired version is greater than allowed
    if _semver.compare(desired_v_max, allowed_v_max) > 0:
        if desired_v_op != '==':
            desired_v_max = allowed_v_max
        else:
            raise _error.PluginDependencyError('{}{} cannot be installed because acceptable version is {}'
                                               .format(plugin_name, desired_v_spec, allowed_versions))

    # If, after above computations, maximum version is lower than minimum
    if _semver.compare(desired_v_min, desired_v_max) > 0:
        desired_v_max = desired_v_min

    # Get available remote plugin info
    try:
        p_remote_info = remote_plugin_info(plugin_name, [
            '>={}'.format(desired_v_min),
            '<={}'.format(desired_v_max),
        ])
    except _error.PluginsApiError as e:
        if e.error_content.startswith('Unknown plugin'):
            raise _error.UnknownPlugin(plugin_name)
        else:
            raise e

    # Version number proposed by server based on plugin_spec
    ver_to_install = p_remote_info['version']  # type: str

    # Check if the plugin is already installed
    try:
        # Update plugin
        l_plugin_info = plugin_package_info(plugin_name)
        if l_plugin_info['version'] != ver_to_install:
            uninstall(plugin_name, True)
        else:
            # Necessary version is already installed, nothing to do
            return installed_count
    except _error.PluginPackageNotFound:
        pass

    # Check if the plugin is not installing at this moment
    if plugin_name in _installing:
        raise _error.PluginInstallationInProgress(plugin_name)

    try:
        # Flag start of the installation process
        _installing.append(plugin_name)
        _console.print_info(_lang.t('pytsite.plugman@installing_plugin', {
            'plugin': '{}-{}'.format(plugin_name, ver_to_install)
        }))
        if _DEBUG:
            _logger.debug("Installation of plugin '{}-{}' started".format(plugin_name, ver_to_install))

        # Create temporary directory to store plugin's content
        tmp_dir_path = _path.join(_reg.get('paths.tmp'), 'plugman')
        if not _path.exists(tmp_dir_path):
            _mkdir(tmp_dir_path, 0o755)

        # Prepare all necessary data
        zip_url = p_remote_info['zip_url']
        tmp_file_path = _path.join(tmp_dir_path, '{}-{}.zip'.format(plugin_name, ver_to_install))

        # Download archive
        if _DEBUG:
            _logger.debug('Downloading {} to {}'.format(zip_url, tmp_file_path))
        _urlretrieve(zip_url, tmp_file_path)
        if _DEBUG:
            _logger.debug('{} successfully stored to {}'.format(zip_url, tmp_file_path))

        # Extract downloaded archive
        if _DEBUG:
            _logger.debug('Extracting {} into {}'.format(tmp_file_path, tmp_dir_path))
        with _zipfile.ZipFile(tmp_file_path) as z_file:
            z_file.extractall(tmp_dir_path)
        if _DEBUG:
            _logger.debug('{} successfully extracted to {}'.format(tmp_file_path, tmp_dir_path))

        # Remove downloaded archive
        _unlink(tmp_file_path)
        if _DEBUG:
            _logger.debug('{} removed'.format(tmp_file_path))

        # Move extracted directory to the plugins directory
        extracted_dir_prefix = '{}-{}{}'.format(_GITHUB_ORG, _GITHUB_PLUGIN_REPO_PREFIX, plugin_name)
        for dir_name in _listdir(tmp_dir_path):
            if not dir_name.startswith(extracted_dir_prefix):
                continue

            source_dir_path = _path.join(tmp_dir_path, dir_name)
            target_dir_path = _plugin_path(plugin_name)

            _rename(source_dir_path, target_dir_path)
            if _DEBUG:
                _logger.debug('{} moved to {}'.format(source_dir_path, target_dir_path))

        # Load installed plugin info
        l_plugin_info = plugin_package_info(plugin_name)

        # Install required pip packages
        for pip_pkg_spec in l_plugin_info['requires']['packages']:
            _console.print_info(_lang.t('pytsite.plugman@plugin_requires_pip_package', {
                'plugin': plugin_name,
                'pip_package': pip_pkg_spec,
            }))
            _install_pip_package(pip_pkg_spec)

        # Install required plugins
        for req_plugin_spec in l_plugin_info['requires']['plugins']:
            if not is_installed(req_plugin_spec):
                _console.print_info(_lang.t('pytsite.plugman@plugin_requires_plugin', {
                    'plugin': plugin_name,
                    'dependency': req_plugin_spec,
                }))
                installed_count += install(req_plugin_spec)

        # Load plugin's module
        plugin = _import_module('plugins.{}'.format(plugin_name))

        # Mark plugin as completely installed
        with open(_path.join(_plugin_path(plugin_name), 'installed'), 'w') as f:
            f.write(str(_datetime.now()))

        # Notify about plugin install
        if hasattr(plugin, 'plugin_install') and callable(plugin.plugin_install):
            plugin.plugin_install()
        _events.fire('pytsite.plugman@install', name=plugin_name)

        # Reload plugin module after all hooks processed
        _reload_module(plugin)

        _console.print_success(_lang.t('pytsite.plugman@plugin_install_success', {
            'plugin': '{}-{}'.format(plugin_name, ver_to_install)
        }))

        return installed_count + 1

    except Exception as e:
        # Remove not completely installed plugin files
        _rmtree(_plugin_path(plugin_name), True)

        raise _error.PluginInstallError(_lang.t('pytsite.plugman@plugin_install_error', {
            'plugin': plugin_name,
            'msg': e,
        }))

    finally:
        _installing.remove(plugin_name)


def uninstall(plugin_name: str, update_mode: bool = False):
    """Uninstall a plugin
    """
    global _uninstalling

    if _DEV_MODE:
        raise _error.PluginUninstallError(_lang.t('pytsite.plugman@cannot_manage_plugins_in_dev_mode'))

    # Check if the plugin is not uninstalling at this moment
    if plugin_name in _uninstalling:
        raise _error.PluginUninstallationInProgress(plugin_name)

    # Check if the plugin is installed
    if not is_installed(plugin_name):
        raise _error.PluginNotInstalled(plugin_name)

    # Check for dependant plugins
    if not update_mode:
        dependants = get_dependant_plugins(plugin_name)
        if dependants:
            raise _error.PluginDependencyError(_lang.t('pytsite.plugman@plugin_has_dependant_plugins', {
                'plugin': plugin_name,
                'dependants': ', '.join(dependants),
            }))

    try:
        _uninstalling.append(plugin_name)

        plugin_version = plugin_package_info(plugin_name)['version']
        _console.print_info(_lang.t('pytsite.plugman@uninstalling_plugin', {
            'plugin': '{}-{}'.format(plugin_name, plugin_version)
        }))

        # Notify about plugin uninstall
        plugin = _import_module('plugins.' + plugin_name)
        if hasattr(plugin, 'plugin_uninstall') and callable(plugin.plugin_uninstall):
            plugin.plugin_uninstall()
        _events.fire('pytsite.plugman@uninstall', name=plugin_name)

        # Delete plugin's files
        _rmtree(_plugin_path(plugin_name))

        _console.print_success(_lang.t('pytsite.plugman@plugin_uninstall_success', {
            'plugin': '{}-{}'.format(plugin_name, plugin_version)
        }))

        # Application should be reloaded to deactivate installed plugin
        _reload.set_flag()

    finally:
        _uninstalling.remove(plugin_name)


def is_dev_mode() -> bool:
    return _DEV_MODE


def on_install(handler, priority: int = 0):
    """Shortcut
    """
    _events.listen('pytsite.plugman@install', handler, priority)


def on_uninstall(handler, priority: int = 0):
    """Shortcut
    """
    _events.listen('pytsite.plugman@uninstall', handler, priority)
