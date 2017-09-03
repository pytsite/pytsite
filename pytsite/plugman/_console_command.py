"""PytSite Plugin Manager Console Commands
"""
from pytsite import console as _console, reload as _reload, package_info as _package_info, theme as _theme
from . import _api, _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Install(_console.Command):
    """plugman:install
    """

    def __init__(self):
        super().__init__()

        self.define_option(_console.option.Bool('reload', default=True))

    @property
    def name(self) -> str:
        return 'plugman:install'

    @property
    def description(self) -> str:
        return 'pytsite.plugman@console_command_description_install'

    def exec(self):
        installed_count = 0

        try:
            if self.args:
                for plugin_spec in self.args:
                    installed_count += _api.install(plugin_spec)
            else:
                # Install plugins required by application
                for plugin_spec in _package_info.requires_plugins('app'):
                    installed_count += _api.install(plugin_spec)

                # Install plugins required by theme
                for plugin_spec in _package_info.requires_plugins(_theme.get().package_name):
                    installed_count += _api.install(plugin_spec)

        except _error.PlugmanError as e:
            raise _console.error.Error(e)

        if installed_count and self.opt('reload'):
            _reload.reload()


class Uninstall(_console.Command):
    """plugman:uninstall
    """

    @property
    def name(self) -> str:
        return 'plugman:uninstall'

    @property
    def description(self) -> str:
        return 'pytsite.plugman@console_command_description_uninstall'

    def exec(self):
        plugin_names = self.args

        if not plugin_names:
            raise _console.error.MissingArgument('pytsite.plugman@plugins_not_specified')

        try:
            for p_name in plugin_names:
                _api.uninstall(p_name)
        except _error.PlugmanError as e:
            raise _console.error.Error(str(e))

        _reload.reload()
