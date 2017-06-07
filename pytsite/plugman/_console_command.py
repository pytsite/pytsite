"""PytSite Plugin Manager Console Commands
"""
from pytsite import console as _console, reg as _reg, reload as _reload, lang as _lang
from . import _api, _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Install(_console.Command):
    """plugman:install
    """

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

        _reload.reload()


class Upgrade(_console.Command):
    """plugman:upgrade
    """

    def __init__(self):
        super().__init__()

        self._define_option(_console.option.Bool('reload', default=True))
        self._define_argument(_console.argument.Argument('plugin_name'))

    @property
    def name(self) -> str:
        return 'plugman:upgrade'

    @property
    def description(self) -> str:
        return 'pytsite.plugman@console_command_description_upgrade'

    def execute(self):
        try:
            _console.print_info(_lang.t('pytsite.plugman@upgrading_plugins'))
            _api.upgrade(self.get_argument_value(0))

        except _error.PluginNotInstalled as e:
            raise _console.error.Error(e)

        if self.get_option_value('reload'):
            _reload.reload()
