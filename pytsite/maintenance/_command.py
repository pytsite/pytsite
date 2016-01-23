"""PytSite Maintenance Console Commands.
"""
from pytsite import console as _console
from . import _function

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Maintenance(_console.command.Abstract):
    """'maintenance' Console Command.
    """
    def get_name(self) -> str:
        """Get name of the command.
        """
        return 'maint'

    def get_description(self) -> str:
        """Get description of the command.
        """
        from pytsite.lang import t
        return t('pytsite.maintenance@maintenance_console_command_description')

    def get_help(self) -> str:
        """Get help for the command.
        """
        return '{} <enable | disable>'.format(self.get_name())

    def execute(self, args: tuple=(), **kwargs):
        """Execute the command.
        """
        if len(args) != 1:
            _console.print_info(self.get_help())
            return 1

        if 'enable' in args:
            _function.enable()
        elif 'disable' in args:
            _function.disable()
        else:
            _console.print_info(self.get_help())
            return 1
