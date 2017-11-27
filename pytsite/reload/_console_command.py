"""PytSite Reload Console Command
"""
from pytsite import console as _console
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Reload(_console.Command):
    """Reload Console Command
    """

    @property
    def name(self) -> str:
        """Get name of the command
        """
        return 'reload'

    @property
    def description(self) -> str:
        """Get description of the command
        """
        return 'pytsite.reload@reload_console_command_description'

    def exec(self):
        """Execute the command
        """
        _api.reload()
