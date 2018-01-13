"""PytSite Plugin Manager
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

# Public API
from sys import meta_path as _meta_path
from os import path as _path
from pytsite import maintenance as _maintenance
from . import _error as error
from ._api import plugins_path, local_plugin_info, install, uninstall, is_installed, load, is_loaded, \
    local_plugins_info, remote_plugin_info, remote_plugins_info, is_dev_mode, get_dependant_plugins, on_install, \
    on_uninstall, plugin_path, is_loading, is_installing, get


class _MetaPathHook:
    def find_spec(self, name: str, import_path: list, module=None):
        name_s = name.split('.')
        if name_s[0] == 'plugins' and len(name_s) == 2 and not is_installing(name_s[1]):
            # Check if the plugin installed
            if not is_installed(name_s[1]):
                raise error.PluginNotInstalled(name_s[1])

            # Check if the plugin loaded
            if not (is_loaded(name_s[1]) or is_loading(name_s[1])):
                raise error.PluginNotLoaded(name_s[1])


def _init():
    from os import mkdir
    from pytsite import lang, console, update
    from . import _console_command

    # Resources
    lang.register_package(__name__)

    # Create 'plugins' package if it doesn't exist
    plugins_dir_path = plugins_path()
    if not _path.exists(plugins_dir_path):
        mkdir(plugins_dir_path, 0o755)
        with open(_path.join(plugins_dir_path, '__init__.py'), 'wt') as f:
            f.write('"""Pytsite Plugins\n"""\n')

    # Register console commands
    console.register_command(_console_command.Install())
    console.register_command(_console_command.Update())
    console.register_command(_console_command.Uninstall())

    # Get information about installed plugins
    plugins_info_seq = local_plugins_info()

    # Enable imports checking
    _meta_path.insert(0, _MetaPathHook())

    # Load installed plugins
    try:
        _maintenance.enable(True)
        
        for p_name in plugins_info_seq:
            if p_name.startswith('_'):
                continue

            try:
                if not is_loaded(p_name):
                    load(p_name)
            except (error.PluginLoadError, error.PluginNotInstalled) as e:
                console.print_warning(e)

    finally:
        _maintenance.disable(True)

    # Event handlers
    update.on_update_after(lambda: console.run_command('plugman:update', {'reload': False}))


_init()
