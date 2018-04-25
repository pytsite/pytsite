"""PytSite Plugin Manager Console Commands
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import subprocess as _subprocess
from pytsite import reload as _reload, console as _console, package_info as _package_info, lang as _lang
from . import _api, _error


class Install(_console.Command):
    """plugman:install
    """

    def __init__(self):
        super().__init__()

        self.define_option(_console.option.Int('stage', default=1))
        self.define_option(_console.option.Int('installed-count', default=0))
        self.define_option(_console.option.Bool('reload', default=True))

    @property
    def name(self) -> str:
        return 'plugman:install'

    @property
    def description(self) -> str:
        return 'pytsite.plugman@console_command_description_install'

    def _get_plugins_specs(self) -> list:
        return self.args if self.args else _package_info.requires_plugins('app')

    def exec(self):
        stage = self.opt('stage')

        if stage == 1:
            installed_count = self.opt('installed-count')

            # Install plugins
            for plugin_spec in self._get_plugins_specs():
                try:
                    installed_count += _api.install(plugin_spec)
                except _error.Error as e:
                    raise _console.error.CommandExecutionError(e)

            if installed_count:
                # Run second stage to let plugins finish installation and update
                p_args = ['./console', self.name, '--stage=2', '--installed-count=' + str(installed_count)]
                return _subprocess.run(p_args).returncode

        elif stage == 2:
            # Do nothing, all work done during plugman init
            if self.opt('reload'):
                _reload.reload()

        else:
            raise _console.error.CommandExecutionError('Invalid stage number')


class Update(Install):
    """plugman:update
    """

    @property
    def name(self) -> str:
        return 'plugman:update'

    @property
    def description(self) -> str:
        return 'pytsite.plugman@console_command_description_update'

    def _get_plugins_specs(self) -> list:
        return self.args if self.args else _api.local_plugins_info().keys()

    def exec(self):
        # Check if the all requested plugins are installed
        for plugin_spec in self._get_plugins_specs():
            if not _api.is_installed(plugin_spec):
                raise _console.error.CommandExecutionError(_lang.t('pytsite.plugman@plugin_not_installed', {
                    'plugin': plugin_spec
                }))

        super().exec()


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
        except _error.Error as e:
            raise _console.error.CommandExecutionError(e)

        _reload.reload()
