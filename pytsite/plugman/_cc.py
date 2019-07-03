"""PytSite Plugin Manager Console Commands
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import re
import subprocess
from pytsite import reload, console, package_info, semver
from . import _api, _error

_PLUGINS_SPEC_RE = re.compile('([a-zA-Z0-9_]+)([<>!=~]*.+)?')


class Install(console.Command):
    """plugman:install
    """

    def __init__(self):
        super().__init__()

        self.define_option(console.option.Int('stage', default=1, maximum=3))
        self.define_option(console.option.Bool('reload', default=True))
        self.define_option(console.option.Bool('no-cache'))

    @property
    def name(self) -> str:
        return 'plugman:install'

    @property
    def description(self) -> str:
        return 'pytsite.plugman@console_command_description_install'

    def exec(self):
        stage = self.opt('stage')

        if stage == 1:
            installed_count = 0
            plugins_specs = {}

            if self.args:
                # Install/update specified plugins
                for p_spec in self.args:
                    match = _PLUGINS_SPEC_RE.findall(p_spec)
                    if not match:
                        raise console.error.CommandExecutionError('Invalid plugin identifier: {}'.format(p_spec))
                    plugins_specs[match[0][0]] = match[0][1]
            else:
                # Install/update all required plugins
                plugins_specs = package_info.requires_plugins('app')

            # Install/update plugins
            for plugin_name, plugin_version in plugins_specs.items():
                try:
                    use_cache = not self.opt('no-cache')
                    installed_count += _api.install(plugin_name, semver.VersionRange(plugin_version), use_cache)
                except _error.Error as e:
                    raise console.error.CommandExecutionError(e)

            # Run second stage to call plugin_install() and plugin_update() hooks for every installed plugin
            if installed_count:
                return subprocess.run(['./console', self.name, '--stage=2']).returncode

        elif stage == 2:
            # At this point trigger _eh.on_pytsite_load() event handler, which calls plugin_install() and
            # plugin_update() for every previously installed plugin.

            # During call to plugin_* hooks some plugins (for example `theming`) can install other plugins,
            # so we need to restart application in console mode in order to call installation hooks of that plugins.
            if _api.get_update_info():
                return subprocess.run(['./console', self.name, '--stage=3']).returncode
            elif self.opt('reload'):
                reload.reload()

        elif stage == 3 and self.opt('reload'):
            # Let all waiting plugins process their hooks and then reload application
            reload.reload()


class Uninstall(console.Command):
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
            raise console.error.MissingArgument('pytsite.plugman@plugins_not_specified')

        try:
            for p_name in self.args:
                _api.uninstall(p_name)
        except _error.Error as e:
            raise console.error.CommandExecutionError(e)

        reload.reload()
