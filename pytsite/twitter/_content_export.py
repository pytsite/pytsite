"""Content Export Drivers.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from twython import Twython as _Twython, TwythonError as _TwithonError
from pytsite import content as _content, content_export
from pytsite.core import widget as _widget, logger as _logger, reg as _reg
from ._widget import Auth as TwitterAuthWidget


class Driver(content_export.AbstractDriver):
    """Content Export Driver.
    """
    def __init__(self, **kwargs):
        """Init.
        """
        self._client_key = _reg.get('twitter.app_key')
        self._client_secret = _reg.get('twitter.app_secret')
        if not self._client_key or not self._client_secret:
            raise Exception("Both 'twitter.app_key' and 'twitter.app_secret' must be defined.")

        self._oauth_token = kwargs.get('oauth_token')
        self._oauth_token_secret = kwargs.get('oauth_token_secret')

    def get_widget(self, uid: str, **kwargs: dict) -> _widget.Base:
        """Get widget for content export edit form.
        """
        return TwitterAuthWidget(uid=uid, **kwargs)

    def export(self, entity: _content.model.Content, exporter=content_export.model.ContentExport):
        """Export data.
        """
        if 'content_export_twitter_' + str(exporter.id) in entity.options:
            _logger.info("{}. '{}' is already exported for this account.".format(__name__, entity.title))
            return

        _logger.info("{}. Export started. '{}'.".format(__name__, entity.title))

        tw = _Twython(self._client_key, self._client_secret, self._oauth_token, self._oauth_token_secret)

        media_ids = []
        if entity.images:
            img = entity.images[0]
            with open(img.abs_path, 'rb') as f:
                r = tw.upload_media(media=f)
                media_ids.append(r['media_id'])

        tags = []
        if entity.tags:
            for tag in entity.tags:
                if tag.title.find(' ') < 0:
                    tag = tag.title
                    tag = '#' + tag
                    tags.append(tag)

        tries = 20
        status = '{} {} {}'.format(entity.title, entity.url, ' '.join(tags))
        while tries:
            try:
                tw.update_status(status=status, media_ids=media_ids)
                entity_opts = entity.options
                entity_opts['content_export_twitter_' + str(exporter.id)] = True
                entity.f_set('options', entity_opts).save()
                break
            except _TwithonError as e:
                # Cut one word from the right
                status = ' '.join(status.split(' ')[:-1])

                tries -= 1
                if not tries:
                    raise e

        _logger.info("{}. Export finished. '{}'.".format(__name__, entity.title))
