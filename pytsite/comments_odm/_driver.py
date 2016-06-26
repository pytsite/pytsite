"""PytSite Comments Abstract Driver.
"""
from typing import Iterable as _Iterable
from pytsite import widget as _widget, auth as _auth, comments as _comments, odm as _odm
from . import _model
from ._widget import Comments as CommentsWidget

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class ODM(_comments.driver.Abstract):
    """Abstract Comments Driver.
    """

    def get_name(self) -> str:
        """Get driver name.
        """
        return 'odm'

    def create_comment(self, thread_id: str, body: str, author: _auth.model.AbstractUser,
                       status: str = 'published') -> _model.Comment:
        """Create new comment.
        """
        pass

    def get_widget(self, widget_uid: str, thread_id: str) -> _widget.Base:
        """Get comments widget for particular thread.
        """
        return CommentsWidget(widget_uid, thread_id=thread_id)

    def get_comments(self, thread_id: str) -> _Iterable[_model.Comment]:
        pass

    def get_comments_count(self, thread_id: str) -> int:
        """Get comments count for particular thread.
        """
        return _odm.find('comment').where('thread_id', '=', thread_id).where('status', '=', 'published').count()
