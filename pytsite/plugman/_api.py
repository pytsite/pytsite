"""PytSite Plugin Manager API
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import zipfile
import requests
import json
import pickle
from typing import Type, Dict, List
from sys import argv
from os import listdir, path, makedirs, unlink, rename
from shutil import rmtree
from importlib import import_module
from urllib.request import urlretrieve
from pytsite import reg, logger, lang, router, console, semver, package_info, cache, reload, events, pip, tpl, util
from . import _error, _cc

_API_CURRENT_VERSION = 2
_API_URLS = reg.get('plugman.api_urls', ['https://plugins.pytsite.xyz'])
_DEV_MODE = router.server_name() == 'local.plugins.pytsite.xyz'

_GITHUB_ORG = 'pytsite'
_GITHUB_PLUGIN_REPO_PREFIX = 'plugin-'
_DEBUG = reg.get('pytsite.debug', False)
_UPDATE_INFO_PATH = path.join(reg.get('paths.storage'), 'plugman.update')

_loading = {}  # type: Dict[str, str]
_loaded = {}  # type: Dict[str, Type]
_faulty = []
_installing = []
_uninstalling = []
_required = set()
_plugman_cache = cache.create_pool('pytsite.plugman')

_PLUGINS_DIR_PATH = path.join(reg.get('paths.root'), 'plugins')
_PLUGINS_PACKAGE_NAME = 'plugins'
_CACHE_TTL = 900  # 15 min

reg.put('paths.plugins', _PLUGINS_DIR_PATH)


def _plugins_api_request(endpoint: str, args: dict = None) -> dict:
    """Do a request to plugins API host
    """
    r = {}

    for base_url in _API_URLS:
        request_url = '{}/api/{}/{}'.format(base_url, _API_CURRENT_VERSION, endpoint)

        if args is None:
            args = {}

        args.update({
            'h': router.server_name(),
        })

        resp = requests.get(request_url, params=args)

        if not resp.ok:
            try:
                raise _error.PluginsApiError(request_url, resp.json().get('error'))
            except json.JSONDecodeError:
                raise _error.PluginsApiError(request_url,
                                             'Error while parsing JSON from string: {}'.format(resp.content))

        r = util.dict_merge(r, resp.json())

    return r


def plugins_dir_path() -> str:
    """Get plugins local directory location
    """
    return _PLUGINS_DIR_PATH


def plugin_path(plugin_name: str) -> str:
    """Calculate local path of a plugin
    """
    return path.join(_PLUGINS_DIR_PATH, plugin_name)


def plugin_json_path(plugin_name: str) -> str:
    """Calculate path to plugin's package JSON file
    """
    return path.join(plugin_path(plugin_name), 'plugin.json')


def plugin_package_name(plugin_name: str) -> str:
    """Calculate plugin package name
    """
    return '{}.{}'.format(_PLUGINS_PACKAGE_NAME, plugin_name)


def local_plugin_info(plugin_name: str, use_cache: bool = True) -> dict:
    """Get information about a local plugin
    """
    try:
        return package_info.data(plugin_json_path(plugin_name), use_cache=use_cache)
    except package_info.error.PackageNotFound:
        raise _error.PluginNotInstalled(plugin_name)


def local_plugins_info(use_cache: bool = True) -> dict:
    """Get information about local plugins
    """
    r = {}
    for plugin_name in listdir(_PLUGINS_DIR_PATH):
        p_path = path.join(_PLUGINS_DIR_PATH, plugin_name)
        if path.isdir(p_path) and not (plugin_name.startswith('.') or plugin_name.startswith('_')):
            r[plugin_name] = local_plugin_info(plugin_name, use_cache)

    return r


def remote_plugins_info(use_cache: bool = True) -> Dict[str, dict]:
    """Get information about remote plugins
    """
    if not use_cache:
        _plugman_cache.clear()

    try:
        data = _plugman_cache.get_hash('remote_plugins')
    except cache.error.KeyNotExist:
        data = _plugman_cache.put_hash('remote_plugins', _plugins_api_request('plugins'), _CACHE_TTL)

    # Sanitize data structures
    n_data = {}
    for p_name, p_data in data.items():
        n_data[p_name] = {}
        for p_ver_str, p_info in p_data.items():
            n_data[p_name][semver.Version(p_ver_str)] = package_info.parse_json(p_info or {})

    return n_data


def remote_plugin_info(plugin_name: str, v_range: semver.VersionRange = None,
                       use_cache: bool = True) -> Dict[semver.Version, dict]:
    """Get information about remote plugin
    """
    p_info = remote_plugins_info(use_cache).get(plugin_name)
    if not p_info:
        raise _error.UnknownPlugin(plugin_name)

    if v_range:
        p_info = {p_ver: p_info[p_ver] for p_ver in p_info.keys() if p_ver in v_range}
        if not p_info:
            raise _error.UnknownPluginVersion(plugin_name, semver.VersionRange(v_range))

    return p_info


def is_installed(plugin_name: str, v_range: semver.VersionRange = None) -> bool:
    """Check if the plugin is installed
    """
    try:
        version = package_info.version(plugin_json_path(plugin_name))
        return version in v_range if v_range else True
    except package_info.error.PackageNotFound:
        return False


def is_being_installed(plugin_name: str) -> bool:
    """Check if the plugin is being installed
    """
    return plugin_name in _installing


def is_loaded(plugin_name: str) -> bool:
    """Check if the plugin is loaded
    """
    return plugin_name in _loaded


def is_loading(plugin_name: str) -> bool:
    """Check if the plugin is being loaded
    """
    return plugin_name in _loading


def get(plugin_name: str) -> object:
    """Get plugin's module object
    """
    try:
        return _loaded[plugin_name]
    except KeyError:
        raise _error.PluginNotLoaded(plugin_name)


def load(plugin_name: str, v_range: semver.VersionRange = None, _required_by: str = None) -> object:
    """Load a plugin
    """
    v_range = v_range or semver.VersionRange()

    # Check if plugin is not faulty
    if plugin_name in _faulty:
        raise _error.PluginLoadError("Plugin '{}' marked as faulty and cannot be loaded".format(plugin_name))

    # Check if the plugin is installed
    if not is_installed(plugin_name, v_range):
        raise _error.PluginNotInstalled('{}{}'.format(plugin_name, v_range), _required_by)

    # Check if the plugin is already loaded
    if plugin_name in _loaded:
        if _DEBUG:
            logger.debug("Plugin '{}' is already loaded".format(plugin_name))
        return _loaded[plugin_name]

    # Check for circular dependency
    if plugin_name in _loading:
        raise _error.CircularDependencyError(plugin_name, _loading[plugin_name])

    # Get info about plugin, but NOT actually load it
    p_info = local_plugin_info(plugin_name)

    # Mark plugin as loading
    _loading[plugin_name] = _required_by

    try:
        # Check required PytSite version
        req_ps_ver = semver.VersionRange(p_info['requires']['pytsite'])
        if package_info.version('pytsite') not in req_ps_ver:
            raise _error.PluginLoadError('pytsite{} is not installed'.format(req_ps_ver))

        # Load required plugins
        for req_p_name, req_p_ver in p_info['requires']['plugins'].items():
            _required.add(req_p_name)
            if _DEBUG:
                logger.debug("Plugin '{}{}' requires '{}{}'".format(plugin_name, v_range, req_p_name, req_p_ver))

            try:
                load(req_p_name, semver.VersionRange(req_p_ver), '{}{}'.format(plugin_name, v_range))
            except _error.PluginLoadError as e:
                raise _error.PluginLoadError("Error while loading dependency for plugin '{}': {}".
                                             format(plugin_name, e))

        # 'pre_load' event
        events.fire('pytsite.plugman@pre_load', name=plugin_name)

        # Import plugin's package
        p_pkg_name = plugin_package_name(plugin_name)
        plugin = import_module(p_pkg_name)

        # Register resource dirs
        for res in ('lang', 'tpl'):
            res_path = path.join(plugin_path(plugin_name), 'res', res)
            if path.isdir(res_path):
                if res == 'lang':
                    lang.register_package(p_pkg_name)
                elif res == 'tpl':
                    tpl.register_package(p_pkg_name)

        # plugin_load() hook
        if hasattr(plugin, 'plugin_load'):
            plugin.plugin_load()

        # plugin_load_{env.type}() hook
        hook_name = 'plugin_load_{}'.format(reg.get('env.type'))
        if hasattr(plugin, hook_name):
            getattr(plugin, hook_name)()

        _loaded[plugin_name] = plugin
        if _DEBUG:
            logger.debug("Plugin '{}{}' loaded".format(plugin_name, p_info['version']))

        # Notify listeners
        events.fire('pytsite.plugman@load', name=plugin_name)

        return plugin

    except Exception as e:
        _faulty.append(plugin_name)
        raise _error.PluginLoadError("Error while loading plugin '{}': {}".format(plugin_name, e))

    finally:
        del _loading[plugin_name]


def _locally_dependant_plugins(plugin_name: str) -> List[str]:
    """Get installed plugin names which are dependant from plugin_name
    """
    if not is_installed(plugin_name):
        raise _error.PluginNotInstalled(plugin_name)

    r = []
    for p_name, p_info in local_plugins_info().items():
        if p_name != plugin_name and plugin_name in p_info['requires']['plugins']:
            r.append(p_name)

    return r


def _download(plugin_name: str, zip_url: str) -> dict:
    """Download and unpack plugin's archive
    """
    # Create a temporary directory to store plugin's files
    tmp_dir_path = path.join(reg.get('paths.tmp'), 'plugman')
    if not path.exists(tmp_dir_path):
        makedirs(tmp_dir_path, 0o755, True)

    # Calculate path to the temporary path of the downloaded archive
    tmp_file_path = path.join(tmp_dir_path, '{}.zip'.format(plugin_name))

    # Download archive
    if _DEBUG:
        logger.debug('Downloading {} to {}'.format(zip_url, tmp_file_path))
    urlretrieve(zip_url, tmp_file_path)
    if _DEBUG:
        logger.debug('{} successfully stored to {}'.format(zip_url, tmp_file_path))

    # Extract downloaded archive
    if _DEBUG:
        logger.debug('Extracting {} into {}'.format(tmp_file_path, tmp_dir_path))
    with zipfile.ZipFile(tmp_file_path) as z_file:
        z_file.extractall(tmp_dir_path)
    if _DEBUG:
        logger.debug('{} successfully extracted to {}'.format(tmp_file_path, tmp_dir_path))

    # Remove downloaded archive
    unlink(tmp_file_path)
    if _DEBUG:
        logger.debug('{} removed'.format(tmp_file_path))

    # Move extracted directory to the plugins directory
    extracted_dir_prefix = '{}-{}{}'.format(_GITHUB_ORG, _GITHUB_PLUGIN_REPO_PREFIX, plugin_name)
    for dir_name in listdir(tmp_dir_path):
        if not dir_name.startswith(extracted_dir_prefix):
            continue

        source_dir_path = path.join(tmp_dir_path, dir_name)
        target_dir_path = plugin_path(plugin_name)

        rename(source_dir_path, target_dir_path)
        if _DEBUG:
            logger.debug('{} moved to {}'.format(source_dir_path, target_dir_path))

    return local_plugin_info(plugin_name, False)


def _install_dependencies(p_info: dict) -> int:
    """Install dependencies for plugin

    Returns a number of installed plugins.
    """
    installed_plugins_count = 0

    # Check for PytSite version
    if package_info.version('pytsite') not in p_info['requires']['pytsite']:
        raise _error.PluginInstallError("Plugin '{}-{}' requires PytSite{}".format(
            p_info['name'], p_info['version'], p_info['requires']['pytsite']))

    # Install required pip packages
    for pip_pkg_name, pip_pkg_version in p_info['requires']['packages'].items():
        pip_pkg_spec = '{}{}'.format(pip_pkg_name, pip_pkg_version)

        if _DEBUG:
            console.print_info(lang.t('pytsite.plugman@plugin_requires_pip_package', {
                'plugin': p_info['name'],
                'pip_package': '{}{}'.format(pip_pkg_name, pip_pkg_version),
            }))

            console.print_info(lang.t('pytsite.plugman@installing_updating_pip_package', {
                'package': pip_pkg_spec
            }))

        pip.install(pip_pkg_name, pip_pkg_version, True, _DEBUG)

        console.print_success(lang.t('pytsite.plugman@pip_package_successfully_installed_updated', {
            'package': pip_pkg_spec
        }))

    # Install required plugins
    for p_name, p_version in p_info['requires']['plugins'].items():
        if _DEBUG:
            console.print_info(lang.t('pytsite.plugman@plugin_requires_plugin', {
                'plugin': p_info['name'],
                'dependency': '{}{}'.format(p_name, p_version),
            }))
        installed_plugins_count += install(p_name, semver.VersionRange(p_version))

    return installed_plugins_count


def install(plugin_name: str, v_range: semver.VersionRange = None, use_cache: bool = True) -> int:
    """Install a plugin

    Returns a number of installed plugins, including dependencies
    """
    global _installing
    installed_count = 0

    # Check for development mode
    if _DEV_MODE:
        raise RuntimeError(lang.t('pytsite.plugman@cannot_manage_plugins_in_dev_mode'))

    # Check if the plugin is not being installed at this moment
    if plugin_name in _installing:
        raise _error.PluginInstallationInProgress(plugin_name)

    # Determine latest available version to install
    p_info = remote_plugin_info(plugin_name, v_range, use_cache)
    v_to_install = semver.last(p_info.keys())
    p_info = p_info[v_to_install]

    # Version to update from
    v_to_update_from = semver.Version()

    try:
        # Check if the required plugin's version is already installed
        l_p_info = local_plugin_info(plugin_name, False)
        if l_p_info['version'] == v_to_install:
            # Necessary version is already installed
            return installed_count
        else:
            # Uninstall current version
            uninstall(plugin_name, True)

            # Schedule plugin update during next application start
            v_to_update_from = l_p_info['version']

    except _error.PluginNotInstalled:
        pass

    try:
        # Mark beginning of the installation process
        _installing.append(plugin_name)

        # Install dependencies
        installed_count += _install_dependencies(p_info)

        # Download and unpack plugin archive
        if _DEBUG:
            console.print_info(lang.t('pytsite.plugman@downloading_plugin', {
                'plugin': '{}-{}'.format(plugin_name, v_to_install)
            }))
        _download(plugin_name, p_info['zip_url'])

        # Schedule call of plugin install/update hooks during next application start
        _set_update_info(plugin_name, v_to_update_from, v_to_install)

        console.print_success(lang.t('pytsite.plugman@plugin_download_success', {
            'plugin': '{}-{}'.format(plugin_name, v_to_install)
        }))

        return installed_count + 1

    except Exception as e:
        # Remove not completely installed plugin files
        rmtree(plugin_path(plugin_name), True)

        events.fire('pytsite.plugman@install_error', name=plugin_name, version=v_to_install, exception=e)

        raise _error.PluginInstallError(lang.t('pytsite.plugman@plugin_download_error', {
            'plugin': plugin_name,
            'msg': e,
        }))

    finally:
        _installing.remove(plugin_name)


def uninstall(plugin_name: str, update_mode: bool = False):
    """Uninstall a plugin
    """
    global _uninstalling

    # No operations in dev mode
    if _DEV_MODE:
        raise _error.PluginUninstallError(lang.t('pytsite.plugman@cannot_manage_plugins_in_dev_mode'))

    # Check if the plugin is not uninstalling at this moment
    if plugin_name in _uninstalling:
        raise _error.PluginUninstallationInProgress(plugin_name)

    # Check if the plugin is installed
    if not is_installed(plugin_name):
        raise _error.PluginNotInstalled(plugin_name)

    # Check for dependant plugins
    if not update_mode:
        dependants = _locally_dependant_plugins(plugin_name)
        if dependants:
            raise _error.PluginDependencyError(lang.t('pytsite.plugman@plugin_has_dependant_plugins', {
                'plugin': plugin_name,
                'dependants': ', '.join(dependants),
            }))

    try:
        _uninstalling.append(plugin_name)

        plugin_version = local_plugin_info(plugin_name, False)['version']

        if _DEBUG:
            console.print_info(lang.t('pytsite.plugman@uninstalling_plugin', {
                'plugin': '{}-{}'.format(plugin_name, plugin_version)
            }))

        # Notify about plugin uninstall
        try:
            plugin = get(plugin_name)
            if hasattr(plugin, 'plugin_uninstall') and callable(plugin.plugin_uninstall):
                plugin.plugin_uninstall()
            events.fire('pytsite.plugman@uninstall', name=plugin_name)

        # Plugin may not be loaded due errors during its startup
        except _error.PluginNotLoaded:
            pass

        # Delete plugin's files
        rmtree(plugin_path(plugin_name))

        console.print_success(lang.t('pytsite.plugman@plugin_uninstall_success', {
            'plugin': '{}-{}'.format(plugin_name, plugin_version)
        }))

        # Application should be reloaded to deactivate installed plugin
        reload.set_flag()

    finally:
        _uninstalling.remove(plugin_name)


def is_dev_mode() -> bool:
    return _DEV_MODE


def on_pre_load(handler, priority: int = 0):
    """Shortcut
    """
    events.listen('pytsite.plugman@pre_load', handler, priority)


def on_load(handler, priority: int = 0):
    """Shortcut
    """
    events.listen('pytsite.plugman@load', handler, priority)


def on_pre_install(handler, priority: int = 0):
    """Shortcut
    """
    events.listen('pytsite.plugman@pre_install', handler, priority)


def on_install(handler, priority: int = 0):
    """Shortcut
    """
    events.listen('pytsite.plugman@install', handler, priority)


def on_install_error(handler, priority: int = 0):
    """Shortcut
    """
    events.listen('pytsite.plugman@install_error', handler, priority)


def on_uninstall(handler, priority: int = 0):
    """Shortcut
    """
    events.listen('pytsite.plugman@uninstall', handler, priority)


def get_update_info(plugin_name: str = None) -> dict:
    def dump_default_file():
        with open(_UPDATE_INFO_PATH, 'wb') as _f:
            _d = {}
            pickle.dump(_d, _f)
        return _d

    if not path.exists(_UPDATE_INFO_PATH):
        d = dump_default_file()
    else:
        with open(_UPDATE_INFO_PATH, 'rb') as f:
            d = pickle.load(f)

    return d.get(plugin_name) if plugin_name else d


def _set_update_info(plugin_name: str, v_from: semver.Version, v_to: semver.Version):
    d = get_update_info()

    d[plugin_name] = {
        'version_from': str(v_from),
        'version_to': str(v_to),
    }

    with open(_UPDATE_INFO_PATH, 'wb') as f:
        pickle.dump(d, f)


def rm_update_info(plugin_name: str):
    d = get_update_info()

    if plugin_name not in d:
        return

    del d[plugin_name]

    with open(_UPDATE_INFO_PATH, 'wb') as f:
        pickle.dump(d, f)


def is_management_mode() -> bool:
    """Check if the plugman is installing, uninstalling or updating plugins now
    """
    cmd_names = [_cc.Install().name, _cc.Uninstall.name]
    for v in argv:
        if v in cmd_names:
            return True

    return False
