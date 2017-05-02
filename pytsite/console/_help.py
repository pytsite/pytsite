"""Help Command.
"""
from . import _command, _api, _argument

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Help(_command.Command):
    """Help Command.
    """

    def __init__(self):
        super().__init__()

        self._define_argument(_argument.Argument('command', required=True))

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

    def execute(self):
        """Execute the command.
        """
        _api.print_info(_api.get_command(self.get_argument_value(0)).signature)
