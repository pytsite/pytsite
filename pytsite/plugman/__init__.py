"""PytSite Plugin Manager
"""
# Public API
from . import _error as error
from ._api import plugins_path, plugin_info, install, uninstall, is_installed, load, is_loaded, \
    plugins_info, remote_plugin_info, remote_plugins_info, is_dev_mode, get_dependant_plugins, \
    get_allowed_version_range, on_install, on_update, on_uninstall

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_plugman_started = False


def _init():
    from os import mkdir, path
    from pytsite import lang, console, update, logger
    from . import _console_command

    # Resources
    lang.register_package(__name__)

    # Create 'plugins' package if it doesn't exist
    plugins_dir_path = plugins_path()
    if not path.exists(plugins_dir_path):
        mkdir(plugins_dir_path, 0o755)
        with open(path.join(plugins_dir_path, '__init__.py'), 'wt') as f:
            f.write('"""Pytsite Plugins\n"""\n')

    # Register console commands
    console.register_command(_console_command.Install())
    console.register_command(_console_command.Update())
    console.register_command(_console_command.Uninstall())

    # Start installed plugins
    for p_name in plugins_info():
        if p_name.startswith('_'):
            continue

        try:
            if not is_loaded(p_name):
                load(p_name)

        except error.PluginLoadError as e:
            logger.error(e)
            console.print_warning(str(e))

    global _plugman_started
    _plugman_started = True

    # Event handlers
    update.on_update_after(lambda: console.run_command('plugman:update', {'reload': False}))


_init()
