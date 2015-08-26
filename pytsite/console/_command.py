"""Console Commands
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from abc import ABC as _ABC, abstractmethod as _abstractmethod


class Abstract(_ABC):
    """Abstract command.
    """
    @_abstractmethod
    def get_name(self) -> str:
        pass

    @_abstractmethod
    def get_description(self) -> str:
        pass

    @_abstractmethod
    def execute(self, **kwargs: dict):
        pass
