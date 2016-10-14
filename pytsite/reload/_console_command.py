"""PytSite Reload Console Commands.
"""
from pytsite import console as _console, lang as _lang
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Reload(_console.command.Abstract):
    """Reload Command.
    """

    def get_name(self) -> str:
        """Get name of the command.
        """
        return 'reload'

    def get_description(self) -> str:
        """Get description of the command.
        """
        return _lang.t('pytsite.reload@reload_console_command_description')

    def execute(self, args: tuple=(), **kwargs):
        _api.reload()
