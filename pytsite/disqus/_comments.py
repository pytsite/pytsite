"""Disqus Comments Driver.
"""
import requests as _requests
from typing import Iterable as _Iterable
from pytsite import reg as _reg, logger as _logger, comments as _comments, auth as _auth
from ._widget import Comments as _DisqusWidget

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Driver(_comments.driver.Abstract):
    """Disqus Comments Driver.
    """
    def get_name(self) -> str:
        """Get driver name.
        """
        return 'disqus'

    def get_widget(self, widget_uid: str, thread_id: str) -> _DisqusWidget:
        """Get comments widget for particular thread.
        """
        return _DisqusWidget(widget_uid)

    def get_comments_count(self, thread_id: str) -> int:
        """Get comments count for particular thread.
        """
        count = 0

        try:
            r = _requests.get('https://disqus.com/api/3.0/forums/listThreads.json', {
                'api_secret': _reg.get('disqus.api_secret'),
                'forum': _reg.get('disqus.short_name'),
                'thread': 'link:' + thread_id,
                'limit': 1,
            }).json()

            if r['code'] == 0 and r['response'] and r['response'][0]['link'] == thread_id:
                count = r['response'][0]['posts']

        except Exception as e:
            _logger.error(str(e), exc_info=e, stack_info=True)

        return count

    def create_comment(self, thread_uid: str, body: str, author: _auth.model.AbstractUser,
                       status: str = 'published', parent_uid: str = None) -> _comments.model.AbstractComment:
        """Create new comment.
        """
        raise NotImplementedError("Not implemented yet.")

    def get_comments(self, thread_uid: str, limit: int = 0, skip: int = 0) \
            -> _Iterable[_comments.model.AbstractComment]:
        raise NotImplementedError("Not implemented yet.")

    def get_comment(self, uid: str) -> _comments.model.AbstractComment:
        """Get single comment by UID.
        """
        raise NotImplementedError("Not implemented yet.")

    def delete_comment(self, uid: str):
        """Mark comment as deleted.
        """
        raise NotImplementedError("Not implemented yet.")

    def get_permissions(self, user: _auth.model.AbstractUser = None) -> dict:
        """Get permissions definition for user.
        """
        raise NotImplementedError("Not implemented yet.")
