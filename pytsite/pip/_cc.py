"""PytSite pip Console Commands
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import re as _re
from pytsite import reg as _reg, console as _console, pip as _pip, package_info as _package_info, lang as _lang

_PKG_SPEC_RE = _re.compile('^([a-zA-Z0-9\-_]+)([~=!<>]+[0-9]+(?:\.[0-9]+)*)?')
_DEBUG = _reg.get('debug')


class Install(_console.Command):
    def __init__(self):
        super().__init__()

        self.define_option(_console.option.Bool('upgrade'))
        self.define_option(_console.option.Bool('debug', default=_DEBUG))

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
        if self.args:
            packages = {}
            for pkg_spec in self.args:
                match = _PKG_SPEC_RE.findall(pkg_spec)
                if not match:
                    raise _console.error.CommandExecutionError('Invalid package identifier: {}'.format(pkg_spec))
                packages[match[0][0]] = match[0][1]
        else:
            packages = _package_info.requires_packages('app').items()

        for pkg_name, pkg_version in packages.items():
            pkg_spec = '{}{}'.format(pkg_name, pkg_version)
            try:
                _console.print_info(_lang.t('pytsite.pip@package_installing', {'package': pkg_spec}))
                _pip.install(pkg_name, pkg_version, self.opt('upgrade'), self.opt('debug'))
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
