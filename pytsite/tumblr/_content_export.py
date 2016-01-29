"""Content Export Tumblr Driver.
"""
from frozendict import frozendict as _frozendict
from pytsite import content as _content, content_export as _content_export, widget as _widget, logger as _logger, \
    form as _form, router as _router
from ._widget import Auth as _TumblrAuthWidget
from ._session import Session as _Session

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Driver(_content_export.AbstractDriver):
    """Content Export Driver.
    """
    def get_name(self) -> str:
        """Get system name of the driver.
        """
        return 'tumblr'

    def get_description(self) -> str:
        """Get human readable description of the driver.
        """
        return 'pytsite.tumblr@tumblr'

    def get_options_description(self, driver_options: _frozendict) -> str:
        """Get human readable driver options.
        """
        return driver_options.get('user_blog')

    def build_settings_form(self, frm: _form.Form, driver_options: _frozendict):
        """Add widgets to the settings form of the driver.
        """
        inp = _router.request().inp
        callback_uri_q = {}
        for k, v in inp.items():
            if not k.startswith('__'):
                callback_uri_q[k] = v

        if '__form_step' in inp:
            callback_uri_q['__form_step'] = inp['__form_step']

        frm.add_widget(_TumblrAuthWidget(
            uid='driver_opts',
            oauth_token=driver_options.get('oauth_token'),
            oauth_token_secret=driver_options.get('oauth_token_secret'),
            screen_name=driver_options.get('screen_name'),
            user_blog=driver_options.get('user_blog'),
            callback_uri=_router.current_url(add_query=callback_uri_q)
        ))

    def export(self, entity: _content.model.Content, exporter=_content_export.model.ContentExport):
        """Export data.
        """
        _logger.info("Export started. '{}'".format(entity.title), __name__)

        try:
            opts = exporter.driver_opts  # type: _frozendict
            oauth_token = opts.get('oauth_token')
            oauth_token_secret = opts.get('oauth_token_secret')

            s = _Session(oauth_token, oauth_token_secret)

            tags = exporter.add_tags  # type: tuple
            tags += tuple(t.title for t in entity.tags)

            thumb_url = entity.images[0].get_url(640) if entity.images else None
            author = entity.author.full_name
            s.blog_post_link(opts['user_blog'], entity.url, entity.title, entity.description, thumb_url,
                             author=author, tags=','.join(tags))
        except Exception as e:
            raise _content_export.error.ExportError(e)

        _logger.info("Export finished. '{}'".format(entity.title), __name__)
