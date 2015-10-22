"""Content Export Tumblr Driver.
"""
from pytsite import content as _content, content_export as _content_export, widget as _widget, logger as _logger, \
    reg as _reg
from ._widget import Auth as TumblrAuthWidget
from ._session import Session

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Driver(_content_export.AbstractDriver):
    """Content Export Driver.
    """
    def __init__(self, **kwargs):
        """Init.
        """
        self._oauth_token = kwargs.get('oauth_token')
        self._oauth_token_secret = kwargs.get('oauth_token_secret')

    def get_settings_widget(self, uid: str, **kwargs: dict) -> _widget.Base:
        """Get widget for content export edit form.
        """
        return TumblrAuthWidget(uid=uid, **kwargs)

    def export(self, entity: _content.model.Content, exporter=_content_export.model.ContentExport):
        """Export data.
        """
        _logger.info("Export started. '{}'".format(entity.title), __name__)

        s = Session(self._oauth_token, self._oauth_token_secret)
        opts = exporter.driver_opts
        """:type: dict"""

        try:
            thumb_url = entity.images[0].get_url(640) if entity.images else None
            author = entity.author.full_name
            tags = ','.join([t.title for t in entity.tags])
            s.blog_post_link(opts['user_blog'], entity.url, entity.title, entity.description, thumb_url,
                             author=author, tags=tags)
        except Exception as e:
            raise _content_export.error.ExportError(e)

        _logger.info("Export finished. '{}'".format(entity.title), __name__)
