"""PytSite pip Console Commands
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import console as _console, pip as _pip, package_info as _package_info, lang as _lang


class Install(_console.Command):
    @property
    def name(self) -> str:
        """Get name of the command
        """
        return 'pip:install'

    @property
    def description(self) -> str:
        """Get description of the command.
        """
        return 'pytsite.pip@install_console_command_description'

    def exec(self):
        for pkg_spec in self.args or _package_info.requires_packages('app'):
            try:
                _console.print_info(_lang.t('pytsite.pip@package_installing', {'package': pkg_spec}))
                _pip.install(pkg_spec)
                _console.print_success(_lang.t('pytsite.pip@package_successfully_installed', {'package': pkg_spec}))
            except _pip.error.Error as e:
                raise _console.error.CommandExecutionError(e)


class Uninstall(_console.Command):
    @property
    def name(self) -> str:
        """Get name of the command
        """
        return 'pip:uninstall'

    @property
    def description(self) -> str:
        """Get description of the command.
        """
        return 'pytsite.pip@uninstall_console_command_description'

    def exec(self):
        if not self.args:
            raise _console.error.MissingArgument('pytsite.pip@package_name_not_specified')

        try:
            for pkg_name in self.args:
                _console.print_info(_pip.uninstall(pkg_name))
        except _pip.error.Error as e:
            raise _console.error.CommandExecutionError(e)
