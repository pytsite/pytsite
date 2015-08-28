"""PytSite Maintenance Console Commands.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import console as _console
from . import _function


class Maintenance(_console.command.Abstract):
    """'maintenance' Console Command.
    """
    def get_name(self) -> str:
        """Get name of the command.
        """
        return 'maintenance'

    def get_description(self) -> str:
        """Get description of the command.
        """
        from pytsite.lang import t
        return t('pytsite.maintenance@maintenance_console_command_description')

    def execute(self, **kwargs: dict):
        """Execute the command.
        """
        if 'enable' in kwargs:
            _function.enable()

        elif 'disable' in kwargs:
            _function.disable()
        else:
            _console.print_info('Usage: app:maintenance --enable | --disable')
