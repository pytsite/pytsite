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

    def get_options_help(self) -> str:
        """Get help for the command.
        """
        return '<command>'

    def execute(self, args: tuple=(), **kwargs):
        """Execute the command.
        :param args:
        """
        for arg in args:
            cmd = _api.get_command(arg)
            _api.print_info('./console {} {}'.format(cmd.get_name(), cmd.get_options_help()))
