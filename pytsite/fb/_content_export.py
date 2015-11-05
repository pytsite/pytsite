"""Facebook Content Export Driver.
"""
from pytsite import content_export as _content_export, logger as _logger, content as _content
from ._widget import Auth as _FacebookAuthWidget
from ._session import Session as _Session

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Driver(_content_export.AbstractDriver):
    def __init__(self, **kwargs):
        """Init.
        """
        self._access_token = kwargs.get('access_token')

    def get_settings_widget(self, uid: str, **kwargs: dict):
        return _FacebookAuthWidget(uid=uid, scope='public_profile,email,user_friends,publish_actions,manage_pages',
                                   **kwargs)

    def export(self, entity: _content.model.Content, exporter=_content_export.model.ContentExport):
        """Export data.
        """
        _logger.info("Export started. '{}'".format(entity.title), __name__)

        s = _Session(self._access_token)
        opts = exporter.driver_opts
        """:type: dict"""

        try:
            thumb_url = entity.images[0].get_url(640) if entity.images else None
            tags = ' '.join(['#' + t.title for t in entity.tags if ' ' not in t.title])
            description = entity.description + ' ' + tags
            user_id = opts['page_id'] if opts['page_id'] else None
            s.feed_link(entity.url, user_id, thumb_url, entity.title, description=description)
        except Exception as e:
            raise _content_export.error.ExportError(e)

        _logger.info("Export finished. '{}'".format(entity.title), __name__)
