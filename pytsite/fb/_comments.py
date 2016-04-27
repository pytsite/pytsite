"""Facebook Comments Driver.
"""
import requests as _requests
from pytsite import comments as _comments, logger as _logger
from ._widget import Comments as _CommentsWidget

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Driver(_comments.Driver):
    """Facebook Comments Driver.
    """
    def __init__(self):
        """Init.
        """

    def get_name(self) -> str:
        """Get driver name.
        """
        return 'fb'

    def get_widget(self, widget_uid: str, thread_id: str) -> _CommentsWidget:
        """Get comments widget for particular thread.
        """
        return _CommentsWidget(widget_uid, href=thread_id)

    def get_comments_count(self, thread_id: str) -> int:
        """Get comments count for particular thread.
        """
        count = 0

        try:
            r = _requests.get('https://graph.facebook.com/v2.4', {
                'fields': 'share{comment_count}',
                'id':  thread_id,
            }).json()

            if 'share' in r:
                count = int(r['share']['comment_count'])

        except Exception as e:
            _logger.error(str(e), __name__)

        return count
