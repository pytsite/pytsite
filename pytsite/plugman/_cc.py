"""PytSite Plugin Manager Console Commands
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import re as _re
import subprocess as _subprocess
from pytsite import reload as _reload, console as _console, package_info as _package_info, events as _events
from . import _api, _error


class Install(_console.Command):
    """plugman:install
    """

    def __init__(self):
        super().__init__()

        self.define_option(_console.option.Int('stage', default=1, maximum=3))
        self.define_option(_console.option.Bool('reload', default=True))

    @property
    def name(self) -> str:
        return 'plugman:install'

    @property
    def description(self) -> str:
        return 'pytsite.plugman@console_command_description_install'

    def exec(self):
        _plugins_spec_re = _re.compile('([^!<>=]+)(.+)')

        stage = self.opt('stage')

        if stage == 1:
            plugins_specs = {}

            if self.args:
                for p_spec in self.args:
                    match = _plugins_spec_re.findall(p_spec)
                    if not match:
                        raise _console.error.CommandExecutionError('Invalid plugin identifier: {}'.format(p_spec))
                    plugins_specs[match[0][0]] = match[0][1]

            # If no plugins to install/update was specified
            else:
                if self.name == 'plugman:install':
                    # Install all plugins required by application
                    plugins_specs = _package_info.requires_plugins('app')
                elif self.name == 'plugman:update':
                    # Update all installed plugins
                    plugins_specs = self.args or _api.local_plugins_info().keys()

            # Install/update plugins
            for plugin_name, plugin_version in plugins_specs.items():
                try:
                    _api.install(plugin_name, plugin_version)
                except _error.Error as e:
                    raise _console.error.CommandExecutionError(e)

            # Notify listeners if command was called without arguments
            if not self.args:
                if self.name == 'plugman:install':
                    _events.fire('pytsite.plugman@install_all')
                elif self.name == 'plugman:update':
                    _events.fire('pytsite.plugman@update_all')

            # Run second stage to call plugin_install() and plugin_update() hooks for every installed plugin
            return _subprocess.run(['./console', self.name, '--stage=2']).returncode

        elif stage == 2:
            # At this point triggers _eh.on_pytsite_load() event handler, which calls plugin_install() and
            # plugin_update() for every previously installed plugin.

            # During call to plugin_* hooks some plugins (for example `theming`) can install other plugins,
            # so we need to restart application in console mode in order to call installation hooks of that plugins.
            if _api.get_update_info():
                return _subprocess.run(['./console', self.name, '--stage=3']).returncode
            else:
                if self.opt('reload'):
                    _reload.reload()

        elif stage == 3:
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
        if not self.args:
            raise _console.error.MissingArgument('pytsite.plugman@plugins_not_specified')

        try:
            for p_name in self.args:
                _api.uninstall(p_name)
        except _error.Error as e:
            raise _console.error.CommandExecutionError(e)

        _reload.reload()
