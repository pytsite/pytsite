"""Facebook Content Export Driver.
"""
import requests as _requests
import re as _re
from pytsite import content_export as _content_export, logger as _logger, content as _content, util as _util
from ._widget import Auth as _FacebookAuthWidget
from ._session import Session as _Session

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


_tag_cleanup_re = _re.compile('[\-_\s]+')


class Driver(_content_export.AbstractDriver):
    def __init__(self, **kwargs):
        """Init.
        """
        super().__init__(**kwargs)

        self._access_token = kwargs.get('access_token')

    def get_settings_widget(self, uid: str, **kwargs):
        scope = 'public_profile,email,user_friends,publish_actions,manage_pages,publish_pages'
        return _FacebookAuthWidget(uid=uid, scope=scope, **kwargs)

    def export(self, entity: _content.model.Content, exporter=_content_export.model.ContentExport):
        """Export data.
        """
        _logger.info("Export started. '{}'".format(entity.title), __name__)

        user_session = _Session(self._access_token)
        opts = exporter.driver_opts
        """:type: dict"""

        try:
            tags = ['#' + _tag_cleanup_re.sub('', t) for t in exporter.add_tags]
            tags += ['#' + _tag_cleanup_re.sub('', t.title) for t in entity.tags]
            message = _util.strip_html_tags(entity.body)[:600] + ' ' + ' '.join(tags) + ' ' + entity.url

            # Pre-generating image for OpenGraph
            if entity.has_field('images') and entity.images:
                _requests.get(entity.images[0].get_url(900, 470))

            if opts['page_id']:
                page_session = _Session(self._get_page_access_token(opts['page_id'], user_session))
                page_session.feed_message(message, entity.url)
            else:
                user_session.feed_message(message, entity.url)
        except Exception as e:
            raise _content_export.error.ExportError(e)

        _logger.info("Export finished. '{}'".format(entity.title), __name__)

    def _get_page_access_token(self, page_id: str, user_session: _Session) -> str:
        """Get page access token.
        """
        for acc in user_session.accounts():
            if 'id' in acc and acc['id'] == page_id:
                return acc['access_token']

        raise Exception('Cannot get access token for page with id == {}'.format(page_id))
