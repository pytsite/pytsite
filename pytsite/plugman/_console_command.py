"""
"""
from pytsite import console as _console, reg as _reg
from . import _api, _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Install(_console.Command):
    def __init__(self):
        super().__init__()

        self._define_argument(_console.argument.Argument('plugin_name'))

    @property
    def name(self) -> str:
        return 'plugman:install'

    @property
    def description(self) -> str:
        return 'pytsite.plugman@console_command_description_install'

    def execute(self):
        plugin_name = self.get_argument_value(0)

        if plugin_name:
            try:
                _api.install(plugin_name)
            except _error.PluginAlreadyInstalled as e:
                raise _console.error.Error(e)

        else:
            # Install required plugins
            for plugin_name in _reg.get('plugman.plugins', set()):
                if not _api.is_installed(plugin_name):
                    _api.install(plugin_name)


class Upgrade(_console.Command):
    def __init__(self):
        super().__init__()

        self._define_argument(_console.argument.Argument('plugin_name'))

    @property
    def name(self) -> str:
        return 'plugman:upgrade'

    @property
    def description(self) -> str:
        return 'pytsite.plugman@console_command_description_upgrade'

    def execute(self):
        plugin_name = self.get_argument_value(0)

        if plugin_name:
            try:
                _api.upgrade(plugin_name)
            except _error.PluginNotInstalled as e:
                raise _console.error.Error(e)
        else:
            # Upgrade all installed plugins
            for name, info in _api.get_plugin_info().items():
                if info.get('installed_version'):
                    _api.upgrade(name)
