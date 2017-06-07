"""PytSite Package Manager API Functions.
"""
import zipfile as _zipfile
import json as _json
import requests as _requests
import subprocess as _subprocess
from typing import Union as _Union
from os import listdir as _listdir, path as _path, mkdir as _mkdir, unlink as _unlink, rename as _rename
from shutil import rmtree as _rmtree
from importlib import import_module as _import_module
from urllib.request import urlretrieve as _urlretrieve
from pytsite import reg as _reg, logger as _logger, reload as _reload, assetman as _assetman, lang as _lang, \
    util as _util, router as _router, console as _console
from . import _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_DEV_MODE = _router.server_name() == 'local.plugins.pytsite.xyz'
_GITHUB_ORG = 'pytsite'
_GITHUB_PLUGIN_REPO_PREFIX = 'plugin-'
_PLUGINS_API_HOST = _reg.get('plugman.api_host', 'plugins.pytsite.xyz')
_PLUGINS_API_URL = _router.scheme() + '://' + _PLUGINS_API_HOST + '/api/1/'
_PLUGINS_API_DEV_HOST = _reg.get('plugman.api_host', 'local.plugins.pytsite.xyz')

_started = []
_installing = []
_uninstalling = []
_erroneous = []
_required = set(_reg.get('plugman.plugins', []))

_PLUGINS_PATH = _path.join(_reg.get('paths.root'), 'plugins')
_PLUGINS_PACKAGE_NAME = 'plugins'


def _get_plugin_path(plugin_name: str) -> str:
    """Calculate local path of a plugin.
    """
    return _path.join(_PLUGINS_PATH, plugin_name)


def _get_plugin_info_path(plugin_name: str) -> str:
    """Calculate local path of a plugin's info file.
    """
    return _path.join(_get_plugin_path(plugin_name), 'plugin.json')


def _read_plugin_json(plugin_name: str) -> dict:
    """Get information about locally installed plugin.
    """
    if not is_installed(plugin_name):
        raise _error.PluginNotInstalled(plugin_name)

    plugin_info_path = _get_plugin_info_path(plugin_name)

    # Load data from plugin.json file
    with open(plugin_info_path, encoding='utf-8') as f:
        data = _json.load(f)  # type: dict

    if not isinstance(data, dict):
        raise TypeError('{} should contain dictionary, got {}'.format(plugin_info_path, type(data)))

    if 'requires' not in data:
        data['requires'] = {'packages': [], 'plugins': []}
    else:
        if 'packages' not in data['requires']:
            data['requires']['packages'] = []
        if 'plugins' not in data['requires']:
            data['requires']['plugins'] = []

    return data


def _write_plugin_json(plugin_name: str, data: dict):
    """Update plugin's info file.
    """
    if not is_installed(plugin_name):
        raise _error.PluginNotInstalled(plugin_name)

    with open(_get_plugin_info_path(plugin_name), 'wt') as f:
        _json.dump(data, f)


def _plugins_api_request(ep: str):
    r = _requests.get(_PLUGINS_API_URL + ep, {
        'h': _router.server_name(),
    })

    if not r.ok:
        raise _error.ApiRequestError(r.content)

    return r.json()


def _install_pip_package(pkg_name: str, upg: bool = False):
    _logger.info('Installing/upgrading pip package: {}'.format(pkg_name))

    cmd = ['pip', 'install', pkg_name]
    if upg:
        cmd.insert(2, '-U')

    r = _subprocess.run(cmd, stdout=_subprocess.PIPE, stderr=_subprocess.PIPE)

    if r.returncode != 0:
        err_msg = r.stderr.decode('utf-8')
        raise _error.PackageInstallError("Pip package '{}' was not installed: {}".format(pkg_name, err_msg))
    else:
        _logger.info('Required package {} has been successfully installed/upgraded'.format(pkg_name))


def get_plugins_path() -> str:
    """Get plugins local directory location.
    """
    return _PLUGINS_PATH


def is_installed(plugin_name: _Union[str, list, tuple]) -> bool:
    """Check if the plugin is installed.
    """
    if isinstance(plugin_name, (list, tuple)):
        for p_name in plugin_name:
            if not is_installed(p_name):
                return False

        return True

    return _path.isdir(_get_plugin_path(plugin_name)) if plugin_name else False


def is_started(plugin_name: str) -> bool:
    """Check if the plugin is started.
    """
    global _started

    return plugin_name in _started


def get_required_plugins() -> set:
    global _required

    return _required


def start(plugin_name: _Union[str, list, tuple]) -> object:
    """Start a plugin.
    """
    global _required, _started

    if isinstance(plugin_name, (list, tuple)):
        for p_name in plugin_name:
            start(p_name)

    if not is_installed(plugin_name):
        raise _error.PluginNotInstalled(plugin_name)

    if plugin_name in _started:
        raise _error.PluginAlreadyStarted(plugin_name)

    if plugin_name in _erroneous:
        raise _error.PluginStartError("Plugin '{}' marked as erroneous and cannot be started.".format(plugin_name))

    # Start required plugins
    for req in _read_plugin_json(plugin_name)['requires']['plugins']:
        _required.add(req)
        if not is_started(req):
            _logger.debug("Plugin '{}' requires '{}'".format(plugin_name, req))
            start(req)

    # Load plugin's package
    pkg_name = _PLUGINS_PACKAGE_NAME + '.' + plugin_name
    try:
        mod = _import_module(pkg_name)
        _started.append(plugin_name)
        _logger.info("Plugin '{}' ({}) started".format(plugin_name, pkg_name))

        return mod

    except Exception as e:
        _erroneous.append(plugin_name)
        raise _error.PluginStartError("Error while starting plugin '{}' ({}): {}".format(plugin_name, pkg_name, e))


def get_remote_plugins() -> dict:
    return _plugins_api_request('plugin/list')


def get_installed_plugins() -> dict:
    r = {}

    for n in _listdir(_PLUGINS_PATH):
        if _path.isdir(_path.join(_PLUGINS_PATH, n)) and not (n.startswith('.') or n.startswith('_')):
            try:
                r[n] = _read_plugin_json(n)
            except FileNotFoundError:
                pass

    return r


def get_plugin_info(plugin_name: str = None) -> dict:
    """Get combined information about remotely available and locally installed plugin(s).
    """
    # Available plugins
    r = _util.dict_merge(get_remote_plugins(), get_installed_plugins())

    for name, info in r.items():
        iv = r[name].get('installed_version')
        lv = r[name].get('latest_version')
        r[name].update({
            'installed_version': iv,
            'latest_version': lv,
            'upgradable': bool(iv and (iv != lv)),
            'required': name in _required,
        })

    if plugin_name:
        try:
            return r[plugin_name]
        except KeyError:
            raise _error.UnknownPlugin("Plugin '{}' does not exist.".format(plugin_name))

    return r


def install(plugin_name: str):
    """Install latest version of a plugin.
    """
    global _installing

    if _DEV_MODE:
        raise RuntimeError(_lang.t('pytsite.plugman@cannot_manage_plugins_in_dev_mode'))

    # Check if the plugin is not installing at this moment
    if plugin_name in _installing:
        raise _error.PluginInstallationInProgress(
            "Installation of the plugin '{}' already started".format(plugin_name))

    # Check if the plugin is already installed
    if is_installed(plugin_name):
        raise _error.PluginAlreadyInstalled(plugin_name)

    try:
        # Flag start of the installation process
        _installing.append(plugin_name)
        _console.print_info(_lang.t('pytsite.plugman@installing_plugin', {'plugin': plugin_name}))
        _logger.debug("Installation of plugin '{}' started".format(plugin_name))

        # Create temporary directory to store plugin's content
        tmp_dir_path = _path.join(_reg.get('paths.tmp'), 'plugman')
        if not _path.exists(tmp_dir_path):
            _mkdir(tmp_dir_path, 0o755)

        # Prepare all necessary data
        plugin_info = get_plugin_info(plugin_name)
        version = plugin_info['latest_version']
        zip_url = plugin_info['zip_url']
        tmp_file_path = _path.join(tmp_dir_path, '{}-{}.zip'.format(plugin_name, version))

        # Download archive
        _logger.debug('Downloading {} to {}'.format(zip_url, tmp_file_path))
        _urlretrieve(zip_url, tmp_file_path)
        _logger.debug('{} successfully stored to {}'.format(zip_url, tmp_file_path))

        # Extract downloaded archive
        _logger.debug('Extracting {} into {}'.format(tmp_file_path, tmp_dir_path))
        with _zipfile.ZipFile(tmp_file_path) as z_file:
            z_file.extractall(tmp_dir_path)
        _logger.debug('{} successfully extracted to {}'.format(tmp_file_path, tmp_dir_path))

        # Remove downloaded archive
        _unlink(tmp_file_path)
        _logger.debug('{} removed'.format(tmp_file_path))

        # Move extracted directory to the plugins directory
        extracted_dir_prefix = '{}-{}{}'.format(_GITHUB_ORG, _GITHUB_PLUGIN_REPO_PREFIX, plugin_name)
        for dir_name in _listdir(tmp_dir_path):
            if not dir_name.startswith(extracted_dir_prefix):
                continue

            source_dir_path = _path.join(tmp_dir_path, dir_name)
            target_dir_path = _get_plugin_path(plugin_name)

            _rename(source_dir_path, target_dir_path)
            _logger.debug('{} moved to {}'.format(source_dir_path, target_dir_path))

            # Store installed version in plugin.json
            local_info = _read_plugin_json(plugin_name)
            local_info.update({
                'installed_version': version,
            })
            _write_plugin_json(plugin_name, local_info)

        # Load plugin info
        info = _read_plugin_json(plugin_name)

        # Install required packages
        for pkg_name in info['requires']['packages']:
            _install_pip_package(pkg_name)

        # Install required plugins
        for plg_name in info['requires']['plugins']:
            if not is_installed(plg_name):
                _logger.info('Installing required plugin: {}'.format(plg_name))
                install(plg_name)

        _console.print_success(_lang.t('pytsite.plugman@plugin_install_success', {
            'plugin': plugin_name,
            'version': version,
        }))

        # Start installed plugin
        if not is_started(plugin_name):
            start(plugin_name)

        # Compile plugin's assets
        if _assetman.is_package_registered(plugin_name):
            _assetman.build(plugin_name)

        # Rebuild translations
        if _lang.is_package_registered(plugin_name):
            _lang.build()

    except Exception as e:
        try:
            uninstall(plugin_name)
        except _error.PluginNotInstalled:
            pass

        msg = _lang.t('pytsite.plugman@plugin_install_error', {
            'plugin': plugin_name,
            'msg': e,
        })

        _console.print_error(msg)

        raise _error.PluginInstallError(msg)

    finally:
        _installing.remove(plugin_name)


def uninstall(plugin_name: str):
    """Uninstall a plugin.
    """
    global _uninstalling

    if _DEV_MODE:
        raise RuntimeError(_lang.t('pytsite.plugman@cannot_manage_plugins_in_dev_mode'))

    # Check if the plugin is not installing at this moment
    if plugin_name in _uninstalling:
        raise _error.PluginUninstallationInProgress(
            "Uninstallation of the plugin '{}' is already started".format(plugin_name))

    if not is_installed(plugin_name):
        raise _error.PluginNotInstalled(plugin_name)

    try:
        _uninstalling.append(plugin_name)

        _console.print_info(_lang.t('pytsite.plugman@uninstalling_plugin', {'plugin': plugin_name}))

        # Delete plugin's files
        _rmtree(_get_plugin_path(plugin_name))

        _console.print_success(_lang.t('pytsite.plugman@plugin_uninstall_success', {'plugin': plugin_name}))

        # Application should be reloaded to deactivate installed plugin
        _reload.set_flag()

    finally:
        _uninstalling.remove(plugin_name)


def upgrade(plugin_name: _Union[None, str, list, tuple] = None):
    """Upgrade a locally installed plugin.
    """
    if _DEV_MODE:
        raise RuntimeError(_lang.t('pytsite.plugman@cannot_manage_plugins_in_dev_mode'))

    # Upgrade all installed plugins
    if plugin_name is None:
        for name, info in get_plugin_info().items():
            if info.get('installed_version'):
                upgrade(name)
        return

    # Upgrade bunch of plugin
    elif isinstance(plugin_name, (list, tuple)):
        for p_name in plugin_name:
            upgrade(p_name)
        return

    if not is_installed(plugin_name):
        raise _error.PluginNotInstalled(plugin_name)

    # Check if the plugin can be upgraded
    info = get_plugin_info(plugin_name)
    if not info['upgradable']:
        return

    _console.print_info(_lang.t('pytsite.plugman@upgrading_plugin', {
        'name': plugin_name,
        'old_ver': info['installed_version'],
        'new_ver': info['latest_version'],
    }))

    # Uninstall current version
    uninstall(plugin_name)

    # Upgrade required plugins
    for required_plugin in info['requires']['plugins']:
        upgrade(required_plugin)

    # Upgrade required packages
    for required_pkg in info['requires']['packages']:
        _install_pip_package(required_pkg, True)

    # Install latest version
    install(plugin_name)


def is_api_host() -> bool:
    return _router.server_name() == _PLUGINS_API_HOST


def is_api_dev_host() -> bool:
    return _router.server_name() == _PLUGINS_API_DEV_HOST
