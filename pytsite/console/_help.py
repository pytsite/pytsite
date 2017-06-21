"""Help Command.
"""
from . import _command, _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Help(_command.Command):
    """Help Command.
    """

    @property
    def name(self) -> str:
        """Get name of the command.
        """
        return 'help'

    @property
    def description(self) -> str:
        """Get description of the command.
        """
        return 'pytsite.console@help_command_description'

    def exec(self):
        """Execute the command.
        """
        _api.print_info(_api.get_command(self.arg(0)).signature)
