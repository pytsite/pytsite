"""oAuth Abstract Driver.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from abc import ABC as _ABC, abstractmethod as _abstractmethod
from pytsite.core import widget as _widget


class Abstract(_ABC):
    """Abstract oAuth session.
    """
    @_abstractmethod
    def get_widget(self, uid: str, **kwargs) -> _widget.Base:
        pass

    @_abstractmethod
    def status_update(self, **kwargs):
        pass
