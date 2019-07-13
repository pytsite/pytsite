"""PytSite Reload Console Commands
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import console
from . import _api


class Reload(console.Command):
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
