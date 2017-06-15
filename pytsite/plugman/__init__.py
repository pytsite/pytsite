"""PytSite Plugin Manager.
"""
# Public API
from . import _error as error
from ._api import get_plugins_path, get_plugin_info, install, uninstall, is_installed, start, is_started, \
    get_installed_plugins, get_remote_plugins, get_required_plugins, is_api_host, is_api_dev_host

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_plugman_started = False


def _init():
    from os import mkdir, path
    from pytsite import settings, lang, assetman, permissions, http_api, logger, console, setup, update
    from . import _settings_form, _eh, _http_api_controllers, _console_command

    # Resources
    lang.register_package(__name__)

    assetman.register_package(__name__)
    assetman.t_less(__name__ + '@**')
    assetman.t_js(__name__ + '@**')

    # Create 'plugins' package
    plugins_path = get_plugins_path()
    if not path.exists(plugins_path):
        mkdir(plugins_path, 0o755)
        with open(path.join(plugins_path, '__init__.py'), 'wt') as f:
            f.write('"""Pytsite Application Plugins.\n"""\n')

    # Console commands
    console.register_command(_console_command.Install())
    console.register_command(_console_command.Upgrade())

    # HTTP API
    http_api.handle('POST', 'plugman/install/<name>', _http_api_controllers.PostInstall(),
                    'pytsite.plugman@post_install')
    http_api.handle('POST', 'plugman/uninstall/<name>', _http_api_controllers.PostUninstall(),
                    'pytsite.plugman@post_uninstall')
    http_api.handle('POST', 'plugman/upgrade/<name>', _http_api_controllers.PostUpgrade(),
                    'pytsite.plugman@post_upgrade')

    if not is_api_dev_host():
        # Permissions
        permissions.define_permission('pytsite.plugman.manage', 'pytsite.plugman@plugin_management', 'app')

        # Settings
        settings.define('plugman', _settings_form.Form, 'pytsite.plugman@plugins', 'fa fa-plug',
                        'pytsite.plugman.manage')

        # Event handlers
        setup.on_setup(_eh.setup, 999)
        update.on_update(_eh.update)
        update.on_update_after(_eh.update_after)

    # Start installed plugins
    for p_name in get_installed_plugins():
        try:
            if not is_started(p_name):
                start(p_name)
        except error.PluginStartError as e:
            logger.error(e, exc_info=e)

    global _plugman_started
    _plugman_started = True


_init()
