"""PytSite Package Manager API
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import zipfile as _zipfile
import requests as _requests
import json as _json
import pickle as _pickle
from typing import Type as _Type, Union as _Union, Dict as _Dict
from os import listdir as _listdir, path as _path, makedirs as _makedirs, unlink as _unlink, rename as _rename
from shutil import rmtree as _rmtree
from importlib import import_module as _import_module
from urllib.request import urlretrieve as _urlretrieve
from pytsite import reg as _reg, logger as _logger, lang as _lang, router as _router, console as _console, \
    semver as _semver, package_info as _package_info, cache as _cache, reload as _reload, events as _events, pip as _pip
from . import _error

_PLUGINS_API_URL = _reg.get('plugman.api_url', 'https://plugins.pytsite.xyz')
_DEV_MODE = _router.server_name() == 'local.plugins.pytsite.xyz'

_GITHUB_ORG = 'pytsite'
_GITHUB_PLUGIN_REPO_PREFIX = 'plugin-'
_DEBUG = _reg.get('plugman.debug', False)
_UPDATE_INFO_PATH = _path.join(_reg.get('paths.storage'), 'plugman.update')

_loading = {}  # type: _Dict[str, str]
_loaded = {}  # type: _Dict[str, _Type]
_faulty = []
_installing = []
_uninstalling = []
_required = set()
_plugman_cache = _cache.create_pool('pytsite.plugman')

_PLUGINS_PATH = _path.join(_reg.get('paths.root'), 'plugins')
_PLUGINS_PACKAGE_NAME = 'plugins'

_reg.put('paths.plugins', _PLUGINS_PATH)


def _sanitize_plugin_name(plugin_name: str) -> str:
    if plugin_name.startswith('plugins.'):
        plugin_name = plugin_name[8:]

    return plugin_name


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


def plugin_path(plugin_name: str) -> str:
    """Calculate local path of a plugin
    """
    return _path.join(_PLUGINS_PATH, _sanitize_plugin_name(plugin_name))


def plugin_json_path(plugin_name: str) -> str:
    """Calculate path to plugin's package JSON file
    """
    return _path.join(plugin_path(plugin_name), 'plugin.json')


def plugins_path() -> str:
    """Get plugins local directory location
    """
    return _PLUGINS_PATH


def local_plugin_info(plugin_name: str, use_cache: bool = True) -> dict:
    """Get information about local plugin
    """
    try:
        plugin_name = _sanitize_plugin_name(plugin_name)

        return _package_info.data(plugin_json_path(plugin_name), defaults={
            'name': 'plugins.{}'.format(plugin_name),
            'version': '0.0.1',
        }, use_cache=use_cache)

    except _package_info.error.PackageNotFound:
        raise _error.PluginPackageNotFound(plugin_name)


def local_plugins_info(use_cache: bool = True) -> dict:
    """Get information about local plugins
    """
    r = {}
    for plugin_name in _listdir(_PLUGINS_PATH):
        p_path = _path.join(_PLUGINS_PATH, plugin_name)
        if _path.isdir(p_path) and not (plugin_name.startswith('.') or plugin_name.startswith('_')):
            r[plugin_name] = local_plugin_info(plugin_name, use_cache)

    return r


def remote_plugin_info(plugin_name: str, versions_spec: list = None):
    """Get information about remote plugin
    """
    versions = ','.join(versions_spec) if versions_spec else '>0.0.0'

    return _plugins_api_request('plugin/{}'.format(_sanitize_plugin_name(plugin_name)), {'version': versions})


def remote_plugins_info() -> dict:
    """Get information about available remote plugins
    """
    try:
        return _plugman_cache.get('remote_plugins')
    except _cache.error.KeyNotExist:
        return _plugman_cache.put('remote_plugins', _plugins_api_request('plugins'), 900)  # 15 min TTL


def is_installed(plugin_spec: _Union[str, list, tuple]) -> bool:
    """Check if the plugin is installed
    """
    if isinstance(plugin_spec, (list, tuple)):
        for p_spec in plugin_spec:
            if not is_installed(p_spec):
                return False

        return True

    plugin_name, version_req = _semver.parse_requirement_str(plugin_spec)
    plugin_name = _sanitize_plugin_name(plugin_name)

    try:
        # Check plugin version
        return _semver.check_conditions(_package_info.version(plugin_json_path(plugin_name)), version_req)
    except _package_info.error.PackageNotFound:
        return False


def is_installing(plugin_name: str) -> bool:
    """Check if trhe plugin is installing
    """
    return _sanitize_plugin_name(plugin_name) in _installing


def is_loaded(plugin_name: str) -> bool:
    """Check if the plugin is loaded
    """
    return _sanitize_plugin_name(plugin_name) in _loaded


def is_loading(plugin_name: str) -> bool:
    """Check if the plugin is being loaded
    """
    return _sanitize_plugin_name(plugin_name) in _loading


def get(plugin_name: str) -> object:
    """Get loaded plugin's module
    """
    try:
        return _loaded[_sanitize_plugin_name(plugin_name)]
    except KeyError:
        raise _error.PluginNotLoaded(plugin_name)


def load(plugin_spec: _Union[str, list, tuple], _required_by_spec: str = None) -> object:
    """Load a plugin
    """
    global _required, _loaded, _loading, _installing, _faulty

    # Multiple load requested
    if isinstance(plugin_spec, (list, tuple)):
        for p_spec in plugin_spec:
            load(p_spec)

    # Normalize plugin spec
    p_name, version_req = _semver.parse_requirement_str(plugin_spec)
    p_name = _sanitize_plugin_name(p_name)
    plugin_spec = '{}{}'.format(p_name, version_req)

    # Check if plugin is not faulty
    if p_name in _faulty:
        raise _error.PluginLoadError("Plugin '{}' marked as faulty and cannot be loaded".format(p_name))

    # Check if the plugin installed
    if not is_installed(plugin_spec):
        raise _error.PluginNotInstalled(plugin_spec, _required_by_spec)

    # Check if the plugin is already loaded
    if p_name in _loaded:
        if _DEBUG:
            _logger.debug("Plugin '{}' already loaded".format(p_name))
        return _loaded[p_name]

    # Check for circular dependency
    if p_name in _loading:
        raise _error.CircularDependencyError(p_name, _loading[p_name])

    # Get info about plugin, but NOT actually load it
    p_info = local_plugin_info(p_name)
    p_version = p_info['version']

    # Mark plugin as loading
    _loading[p_name] = _required_by_spec

    try:
        # Load required plugins
        for req_plugin_spec_str in p_info['requires']['plugins']:
            req_p_spec = _semver.parse_requirement_str(req_plugin_spec_str)
            _required.add(req_p_spec[0])
            if _DEBUG:
                _logger.debug("Plugin '{}-{}' requires '{}{}'".format(p_name, p_version, req_p_spec[0], req_p_spec[1]))
            try:
                load(req_plugin_spec_str, '{}-{}'.format(p_name, p_version))
            except _error.PluginLoadError as e:
                raise _error.PluginLoadError('Error while loading dependency for {}: {}'.format(plugin_spec, e))

        # Import plugin's package
        plugin = _import_module(_PLUGINS_PACKAGE_NAME + '.' + p_name)

        # plugin_load() hook
        if hasattr(plugin, 'plugin_load') and callable(plugin.plugin_load):
            plugin.plugin_load()

        # plugin_load_{env.type}() hook
        env_type = _reg.get('env.type')
        hook_names = ['plugin_load_{}'.format(env_type)]
        if env_type == 'wsgi':
            hook_names.append('plugin_load_uwsgi')
        for hook_name in hook_names:
            if hasattr(plugin, hook_name):
                getattr(plugin, hook_name)()

        _loaded[p_name] = plugin
        if _DEBUG:
            _logger.debug("Plugin '{}-{}' loaded".format(p_name, p_info['version']))

        return plugin

    except Exception as e:
        _faulty.append(p_name)
        raise _error.PluginLoadError("Error while loading plugin {}: {}".format(p_name, e))

    finally:
        del _loading[p_name]


def get_dependant_plugins(plugin_name: str) -> list:
    """Get locally installed plugin names which are dependant from plugin_name
    """
    plugin_name = _sanitize_plugin_name(plugin_name)

    if not is_installed(plugin_name):
        raise _error.PluginNotInstalled(plugin_name)

    r = []
    for p_name, p_info in local_plugins_info().items():
        if p_name != plugin_name and plugin_name in p_info['requires']['plugins']:
            r.append(p_name)

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

    # Get desired minimum and maximum versions
    desired_v_min = _semver.minimum(desired_v_spec)
    desired_v_max = _semver.maximum(desired_v_spec)

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
        # Schedule plugin update for next application start
        l_plugin_info = local_plugin_info(plugin_name, False)
        if l_plugin_info['version'] != ver_to_install:
            _set_update_info(plugin_name, l_plugin_info['version'], ver_to_install)
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
            _makedirs(tmp_dir_path, 0o755, True)

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
            target_dir_path = plugin_path(plugin_name)

            _rename(source_dir_path, target_dir_path)
            if _DEBUG:
                _logger.debug('{} moved to {}'.format(source_dir_path, target_dir_path))

        # Get unpacked plugin info
        l_plugin_info = local_plugin_info(plugin_name, False)

        # Check for PytSite version
        if not _semver.check_conditions(_package_info.version('pytsite'), l_plugin_info['requires']['pytsite']):
            raise _error.PluginInstallError("Plugin '{}-{}' requires PytSite{}".format(
                plugin_name, l_plugin_info['version'], l_plugin_info['requires']['pytsite']))

        # Install required pip packages
        for pip_pkg_spec in l_plugin_info['requires']['packages']:
            _console.print_info(_lang.t('pytsite.plugman@plugin_requires_pip_package', {
                'plugin': plugin_name,
                'pip_package': pip_pkg_spec,
            }))

            _console.print_info(_lang.t('pytsite.plugman@installing_upgrading_pip_package', {
                'package': pip_pkg_spec
            }))

            _pip.install(pip_pkg_spec, _pip.is_installed(pip_pkg_spec))

            _console.print_success(_lang.t('pytsite.plugman@pip_package_successfully_installed_upgraded', {
                'package': pip_pkg_spec
            }))

        # Install required plugins
        for req_plugin_spec in l_plugin_info['requires']['plugins']:
            if not is_installed(req_plugin_spec):
                _console.print_info(_lang.t('pytsite.plugman@plugin_requires_plugin', {
                    'plugin': plugin_name,
                    'dependency': req_plugin_spec,
                }))
                installed_count += install(req_plugin_spec)

        # Plan to call installation hooks for next application start
        if not get_update_info(plugin_name):
            _set_update_info(plugin_name, '0.0.1', ver_to_install)

        _console.print_success(_lang.t('pytsite.plugman@plugin_install_success', {
            'plugin': '{}-{}'.format(plugin_name, ver_to_install)
        }))

        return installed_count + 1

    except Exception as e:
        # Remove not completely installed plugin files
        _rmtree(plugin_path(plugin_name), True)

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

    plugin_name = _sanitize_plugin_name(plugin_name)

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

        plugin_version = local_plugin_info(plugin_name, False)['version']
        _console.print_info(_lang.t('pytsite.plugman@uninstalling_plugin', {
            'plugin': '{}-{}'.format(plugin_name, plugin_version)
        }))

        # Notify about plugin uninstall
        try:
            plugin = get(plugin_name)
            if hasattr(plugin, 'plugin_uninstall') and callable(plugin.plugin_uninstall):
                plugin.plugin_uninstall()
            _events.fire('pytsite.plugman@uninstall', name=plugin_name)

        # Plugin may not be loaded due errors during its startup
        except _error.PluginNotLoaded:
            pass

        # Delete plugin's files
        _rmtree(plugin_path(plugin_name))

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


def on_update(handler, priority: int = 0):
    """Shortcut
    """
    _events.listen('pytsite.plugman@update', handler, priority)


def on_uninstall(handler, priority: int = 0):
    """Shortcut
    """
    _events.listen('pytsite.plugman@uninstall', handler, priority)


def get_update_info(plugin_name: str = None) -> dict:
    def dump_default_file():
        with open(_UPDATE_INFO_PATH, 'wb') as _f:
            _d = {}
            _pickle.dump(_d, _f)
        return _d

    if not _path.exists(_UPDATE_INFO_PATH):
        d = dump_default_file()
    else:
        with open(_UPDATE_INFO_PATH, 'rb') as f:
            d = _pickle.load(f)

    return d.get(plugin_name) if plugin_name else d


def _set_update_info(plugin_name: str, version_from: str, version_to: str):
    d = get_update_info()

    d[plugin_name] = {
        'version_from': version_from,
        'version_to': version_to,
    }

    with open(_UPDATE_INFO_PATH, 'wb') as f:
        _pickle.dump(d, f)


def rm_update_info(plugin_name: str):
    d = get_update_info()

    if plugin_name not in d:
        return

    del d[plugin_name]

    with open(_UPDATE_INFO_PATH, 'wb') as f:
        _pickle.dump(d, f)
