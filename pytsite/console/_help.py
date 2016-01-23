"""Help Command.
"""
from . import _command, _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Help(_command.Abstract):
    """Help Command.
    """
    def get_name(self) -> str:
        """Get name of the command.
        """
        return 'help'

    def get_description(self) -> str:
        """Get description of the command.
        """
        from pytsite import lang
        return lang.t('pytsite.console@help_command_description')

    def get_help(self) -> str:
        """Get help for the command.
        """
        return '{} <command>'.format(self.get_name())

    def execute(self, args: tuple=(), **kwargs):
        """Execute the command.
        :param args:
        """
        if not args:
            _api.print_info(self.get_help())

        _api.print_info(_api.get_command(args[0]).get_help())
