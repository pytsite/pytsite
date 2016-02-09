"""Console Commands
"""
from abc import ABC as _ABC, abstractmethod as _abstractmethod

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Abstract(_ABC):
    """Abstract command.
    """
    @_abstractmethod
    def get_name(self) -> str:
        """Get name of the command.
        """
        pass

    @_abstractmethod
    def get_description(self) -> str:
        """Get description of the command.
        """
        pass

    def get_options_help(self) -> str:
        """Get help for the command.
        """
        return ''

    def get_options(self) -> tuple:
        return ()

    @_abstractmethod
    def execute(self, args: tuple=(), **kwargs):
        """Execute the command.
        """
        pass
