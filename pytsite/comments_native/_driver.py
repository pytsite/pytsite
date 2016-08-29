"""PytSite Comments Abstract Driver.
"""
from typing import Iterable as _Iterable
from pytsite import widget as _widget, auth as _auth, comments as _comments, odm as _odm, odm_auth as _odm_auth
from ._widget import Comments as _CommentsWidget

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Native(_comments.driver.Abstract):
    """Abstract Comments Driver.
    """

    def get_name(self) -> str:
        """Get driver name.
        """
        return 'native'

    def create_comment(self, thread_uid: str, body: str, author: _auth.model.AbstractUser, status: str = 'published',
                       parent_uid: str = None) -> _comments.model.AbstractComment:
        """Create new comment.
        """
        body = body.strip()

        comment = _odm.dispense('comment')
        comment.f_set('thread_uid', thread_uid)
        comment.f_set('body', body)
        comment.f_set('author', author)
        comment.f_set('status', status)
        comment.save()

        if parent_uid:
            parent = _odm.get_by_ref('comment:' + parent_uid)
            if parent.depth == _comments.get_comment_max_depth():
                raise RuntimeError('Comment max depth exceeded.')

            with parent:
                c_user = _auth.get_current_user()
                _auth.switch_user(_auth.get_system_user())
                parent.append_child(comment).save()
                _auth.switch_user(c_user)

        return comment

    def get_widget(self, widget_uid: str, thread_id: str) -> _widget.Abstract:
        """Get comments widget for particular thread.
        """
        return _CommentsWidget(widget_uid, thread_id=thread_id)

    def get_comments(self, thread_uid: str, limit: int = 0, skip: int = 0) \
            -> _Iterable[_comments.model.AbstractComment]:
        """Get comments.
        """
        f = _odm.find('comment').where('thread_uid', '=', thread_uid)

        return f.sort([('publish_time', _odm.I_ASC)]).skip(skip).get(limit)

    def get_comment(self, uid: str) -> _comments.model.AbstractComment:
        """Get single comment by UID.
        """
        comment = _odm.find('comment').where('_id', '=', uid).first()

        if not comment:
            raise _comments.error.CommentNotExist("Comment '{}' not exist.".format(uid))

        return comment

    def get_comments_count(self, thread_uid: str) -> int:
        """Get comments count for particular thread.
        """
        return _odm.find('comment').where('thread_uid', '=', thread_uid).where('status', '=', 'published').count()

    def delete_comment(self, uid: str):
        """Mark comment as deleted.
        """
        comment = _odm.find('comment').where('_id', '=', uid).first()
        if not comment:
            raise _comments.error.CommentNotExist("Comment '{}' does not exist.".format(uid))

        with comment:
            comment.f_set('status', 'deleted').save()

    def get_permissions(self, user: _auth.model.AbstractUser = None) -> dict:
        """Get permissions definition for user.
        """
        return {
            'create': _odm_auth.check_permissions('create', 'comment', user)
        }