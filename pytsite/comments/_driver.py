"""PytSite Comments Abstract Driver.
"""
from typing import Iterable as _Iterable
from abc import ABC as _ABC, abstractmethod as _abstractmethod
from pytsite import widget as _widget, auth as _auth
from . import _model

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Abstract(_ABC):
    """Abstract Comments Driver.
    """

    @_abstractmethod
    def get_name(self) -> str:
        """Get driver name.
        """
        pass

    @_abstractmethod
    def create_comment(self, thread_uid: str, body: str, author: _auth.model.AbstractUser,
                       status: str = 'published', parent_uid: str = None) -> _model.AbstractComment:
        """Create new comment.
        """
        pass

    @_abstractmethod
    def get_widget(self, widget_uid: str, thread_uid: str) -> _widget.Abstract:
        """Get comments widget.
        """
        pass

    @_abstractmethod
    def get_comments(self, thread_uid: str, limit: int = 0, skip: int = 0) -> _Iterable[_model.AbstractComment]:
        """Get comments.
        """
        pass

    @_abstractmethod
    def get_comment(self, uid: str) -> _model.AbstractComment:
        """Get single comment by UID.
        """
        pass

    @_abstractmethod
    def get_comments_count(self, thread_uid: str) -> int:
        """Get comments count for particular thread.
        """
        pass

    @_abstractmethod
    def delete_comment(self, uid: str):
        """Mark comment as deleted.
        """
        pass

    @_abstractmethod
    def delete_thread(self, thread_uid: str):
        """Physically remove comments for particular thread.
        """
        pass

    @_abstractmethod
    def get_permissions(self, user: _auth.model.AbstractUser = None) -> dict:
        """Get permissions definition for user.
        """
        pass
