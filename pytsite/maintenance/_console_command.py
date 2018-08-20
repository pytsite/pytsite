"""PytSite Maintenance Console Commands
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import console as _console
from . import _api


class Maintenance(_console.Command):
    """'maintenance' Console Command
    """

    @property
    def name(self) -> str:
        """Get name of the command.
        """
        return 'maint'

    @property
    def description(self) -> str:
        """Get description of the command.
        """
        return 'pytsite.maintenance@maintenance_console_command_description'

    def exec(self):
        """Execute the command.
        """
        action = self.arg(0)

        if action == 'enable':
            _api.enable()
        elif action == 'disable':
            _api.disable()
        else:
            raise _console.error.InvalidArgument(0, action)
