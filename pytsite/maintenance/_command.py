"""PytSite Maintenance Console Commands.
"""
from pytsite import console as _console, validation as _validation
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

    def get_options_help(self) -> str:
        """Get help for the command.
        """
        return '--enable | --disable>'

    def get_options(self) -> tuple:
        """Get command options.
        """
        return (
            ('enable', _validation.rule.Dummy()),
            ('disable', _validation.rule.Dummy())
        )

    def execute(self, args: tuple=(), **kwargs):
        """Execute the command.
        """
        if not kwargs:
            raise _console.error.InsufficientArguments()

        for arg in kwargs:
            if arg == 'enable':
                _function.enable()
            if arg == 'disable':
                _function.disable()
