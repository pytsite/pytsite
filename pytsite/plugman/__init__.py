"""PytSite Plugin Manager.
"""
# Public API
from sys import exit as _exit
from . import _error as error
from ._api import plugins_path, plugin_info, install, uninstall, is_installed, start, is_started, \
    plugins_info, remote_plugin_info, remote_plugins_info, is_dev_mode, get_dependant_plugins, \
    get_allowed_version_range

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_plugman_started = False


def _init():
    from os import mkdir, path
    from pytsite import settings, lang, assetman, permissions, http_api, console, setup, update
    from . import _settings_form, _http_api_controllers, _console_command

    # Resources
    lang.register_package(__name__)

    assetman.register_package(__name__)
    assetman.t_less(__name__ + '@**')
    assetman.t_js(__name__ + '@**')

    # Create 'plugins' package
    plugins_dir_path = plugins_path()
    if not path.exists(plugins_dir_path):
        mkdir(plugins_dir_path, 0o755)
        with open(path.join(plugins_dir_path, '__init__.py'), 'wt') as f:
            f.write('"""Pytsite Application Plugins.\n"""\n')

    # Console commands
    console.register_command(_console_command.Install())
    console.register_command(_console_command.Update())
    console.register_command(_console_command.Uninstall())

    # HTTP API
    http_api.handle('POST', 'plugman/install/<name>', _http_api_controllers.PostInstall(),
                    'pytsite.plugman@post_install')
    http_api.handle('POST', 'plugman/uninstall/<name>', _http_api_controllers.PostUninstall(),
                    'pytsite.plugman@post_uninstall')
    http_api.handle('POST', 'plugman/upgrade/<name>', _http_api_controllers.PostUpgrade(),
                    'pytsite.plugman@post_upgrade')

    if not is_dev_mode():
        # Permissions
        permissions.define_permission('pytsite.plugman.manage', 'pytsite.plugman@plugin_management', 'app')

        # Settings
        settings.define('plugman', _settings_form.Form, 'pytsite.plugman@plugins', 'fa fa-plug',
                        'pytsite.plugman.manage')

        # Event handlers
        setup.on_setup(lambda: console.run_command('plugman:install', {'reload': False}), 999)
        update.on_update_after(lambda: console.run_command('plugman:update', {'reload': False}))

    # Start installed plugins
    for p_name in plugins_info():
        try:
            if not is_started(p_name):
                start(p_name)
        except error.PluginStartError as e:
            console.print_error(str(e), exc_info=e)
            _exit(1)

    global _plugman_started
    _plugman_started = True


_init()
