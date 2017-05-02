"""PytSite Maintenance Console Commands.
"""
from pytsite import console as _console
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Maintenance(_console.Command):
    """'maintenance' Console Command.
    """

    def __init__(self):
        super().__init__()

        self._define_argument(_console.argument.Choice('action', True, options=['enable', 'disable']))

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

    def execute(self, args: tuple = (), **kwargs):
        """Execute the command.
        """
        action = self.get_argument_value(0)

        if action == 'enable':
            _api.enable()
        if action == 'disable':
            _api.disable()
