"""PytSite pip Support Console Commands
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import re
from pytsite import reg, console, pip, package_info, lang

_PKG_SPEC_RE = re.compile('^([a-zA-Z0-9\\-_]+)([~=!<>]+[0-9]+(?:\\.[0-9]+)*)?')
_DEBUG = reg.get('debug')


class List(console.Command):
    @property
    def name(self) -> str:
        """Get name of the command
        """
        return 'pip:list'

    @property
    def description(self) -> str:
        """Get description of the command.
        """
        return 'pytsite.pip@list_console_command_description'

    def __init__(self):
        super().__init__()

        self.define_option(console.option.Bool('outdated'))

    def exec(self):
        for data in pip.ls(self.opt('outdated')):
            r = f"{data['name']} {data['version']}"

            if 'latest_version' in data:
                r += f" ({data['latest_version']} available)"

            console.print_info(r)


class Install(console.Command):
    def __init__(self):
        super().__init__()

        self.define_option(console.option.Bool('upgrade'))
        self.define_option(console.option.Bool('debug', default=_DEBUG))

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
                    raise console.error.CommandExecutionError('Invalid package identifier: {}'.format(pkg_spec))
                packages[match[0][0]] = match[0][1]
        else:
            packages = package_info.requires_packages('app').items()

        for pkg_name, pkg_version in packages.items():
            pkg_spec = '{}{}'.format(pkg_name, pkg_version)
            try:
                console.print_info(lang.t('pytsite.pip@package_installing', {'package': pkg_spec}))
                pip.install(pkg_name, pkg_version, self.opt('upgrade'), self.opt('debug'))
                console.print_success(lang.t('pytsite.pip@package_successfully_installed', {'package': pkg_spec}))
            except pip.error.Error as e:
                raise console.error.CommandExecutionError(e)


class Uninstall(console.Command):
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
            raise console.error.MissingArgument('pytsite.pip@package_name_not_specified')

        try:
            for pkg_name in self.args:
                console.print_info(pip.uninstall(pkg_name))
        except pip.error.Error as e:
            raise console.error.CommandExecutionError(e)
