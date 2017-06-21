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

    @property
    def name(self) -> str:
        return 'plugman:install'

    @property
    def description(self) -> str:
        return 'pytsite.plugman@console_command_description_install'

    def exec(self):
        try:
            try:
                _api.install(self.arg(0))
            except _error.PluginAlreadyInstalled as e:
                raise _console.error.Error(e)
        except _console.error.MissingArgument:
            # Install required plugins
            for plugin_name in _reg.get('plugman.plugins', []):
                if not _api.is_installed(plugin_name):
                    _api.install(plugin_name)

        _reload.reload()


class Upgrade(_console.Command):
    """plugman:upgrade
    """

    def __init__(self):
        super().__init__()

        self.define_option(_console.option.Bool('reload', default=True))

    @property
    def name(self) -> str:
        return 'plugman:upgrade'

    @property
    def description(self) -> str:
        return 'pytsite.plugman@console_command_description_upgrade'

    def exec(self):
        try:
            _console.print_info(_lang.t('pytsite.plugman@upgrading_plugins'))
            _api.upgrade(self.arg(0))

        except _error.PluginNotInstalled as e:
            raise _console.error.Error(e)

        if self.opt('reload'):
            _reload.reload()
