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

    def exec(self):
        installed_count = self.opt('installed-count')

        try:
            if self.args:
                for plugin_spec in self.args:
                    installed_count += _api.install(plugin_spec)
            else:
                # Install plugins required by application
                for plugin_spec in _package_info.requires_plugins('app'):
                    installed_count += _api.install(plugin_spec)

        except _error.Error as e:
            raise _console.error.CommandExecutionError(e)

        if installed_count:
            if self.opt('stage') == 1:
                # Run second stage to let plugins finish installation and update
                r = _subprocess.run(['./console', self.name, '--stage=2', '--installed-count=' + str(installed_count)])
                return r.returncode
            elif self.opt('reload'):
                _reload.reload()


class Update(_console.Command):
    """plugman:update
    """

    def __init__(self):
        super().__init__()

        self.define_option(_console.option.Int('stage', default=1))
        self.define_option(_console.option.Int('installed-count', default=0))
        self.define_option(_console.option.Bool('reload', default=True))

    @property
    def name(self) -> str:
        return 'plugman:update'

    @property
    def description(self) -> str:
        return 'pytsite.plugman@console_command_description_update'

    def exec(self):
        installed_count = self.opt('installed-count')

        try:
            if self.args:
                # Update specified plugins
                for plugin_spec in self.args:
                    if not _api.is_installed(plugin_spec):
                        raise _console.error.CommandExecutionError(_lang.t('pytsite.plugman@plugin_not_installed', {
                            'plugin': plugin_spec
                        }))
                    installed_count += _api.install(plugin_spec)
            else:
                # Update all installed plugins
                for plugin_spec in _api.local_plugins_info():
                    installed_count += _api.install(plugin_spec)

        except _error.Error as e:
            raise _console.error.CommandExecutionError(e)

        if installed_count:
            if self.opt('stage') == 1:
                # Run second stage to let plugins finish installation and update
                r = _subprocess.run(['./console', self.name, '--stage=2', '--installed-count=' + str(installed_count)])
                return r.returncode
            elif self.opt('reload'):
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
        except _error.Error as e:
            raise _console.error.CommandExecutionError(e)

        _reload.reload()
