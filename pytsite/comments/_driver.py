"""PytSite Comments Abstract Driver.
"""
from abc import ABC as _ABC, abstractmethod as _abstractmethod
from pytsite import widget as _widget

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Driver(_ABC):
    """Abstract Comments Driver.
    """
    @_abstractmethod
    def get_name(self) -> str:
        """Get driver name.
        """
        pass

    @_abstractmethod
    def get_widget(self, widget_uid: str, thread_id: str) -> _widget.Base:
        """Get comments widget for particular thread.
        """
        pass

    @_abstractmethod
    def get_comments_count(self, thread_id: str) -> int:
        """Get comments count for particular thread.
        """
        pass
