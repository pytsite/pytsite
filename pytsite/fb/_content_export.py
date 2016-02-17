"""Facebook Content Export Driver.
"""
import requests as _requests
import re as _re
from frozendict import frozendict as _frozendict
from pytsite import content_export as _content_export, logger as _logger, content as _content, util as _util, \
    form as _form, router as _router
from ._widget import Auth as _FacebookAuthWidget
from ._session import Session as _Session
from . import _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


_tag_cleanup_re = _re.compile('[\-_\s]+')


class Driver(_content_export.AbstractDriver):
    def get_name(self) -> str:
        """Get system name of the driver.
        """
        return 'fb'

    def get_description(self):
        """Get human readable description of the driver.
        """
        return 'pytsite.fb@facebook'

    def build_settings_form(self, frm: _form.Form, driver_options: _frozendict):
        """Add widgets to the settings form of the driver.
        """
        inp = _router.request().inp
        redirect_url_q = {}
        for k, v in inp.items():
            if not k.startswith('__'):
                redirect_url_q[k] = v

        if '__form_step' in inp:
            redirect_url_q['__form_step'] = inp['__form_step']

        frm.add_widget(_FacebookAuthWidget(
            weight=10,
            uid='driver_opts',
            scope='public_profile,email,user_friends,publish_actions,manage_pages,publish_pages',
            form_steps=2,
            access_token=driver_options.get('access_token'),
            access_token_type=driver_options.get('access_token_type'),
            access_token_expires=driver_options.get('access_token_expires'),
            user_id=driver_options.get('user_id'),
            page_id=driver_options.get('page_id'),
            screen_name=driver_options.get('screen_name'),
            redirect_url=_router.current_url(add_query=redirect_url_q),
        ))

    def get_options_description(self, driver_options: _frozendict) -> str:
        """Get driver options as a string.
        """
        r = driver_options.get('screen_name')
        if 'page_id' in driver_options and driver_options['page_id']:
            r += ' (page {})'.format(driver_options.get('page_id'))

        return r

    def export(self, entity: _content.model.Content, exporter=_content_export.model.ContentExport):
        """Export data.
        """
        _logger.info("Export started. '{}'".format(entity.title), __name__)

        try:
            opts = exporter.driver_opts  # type: _frozendict
            user_session = _Session(opts.get('access_token'))

            # Tags
            tags = ['#' + _tag_cleanup_re.sub('', t) for t in exporter.add_tags]
            tags += ['#' + _tag_cleanup_re.sub('', t.title) for t in entity.tags]
            message = _util.strip_html_tags(entity.body)[:600] + ' ' + ' '.join(tags) + ' ' + entity.url

            # Pre-generating image for OpenGraph story
            if entity.has_field('images') and entity.images:
                _requests.get(entity.images[0].get_url(900, 500))

            # Notify OpenGraph about sharing
            scrape_r = user_session.request('', 'POST', id=entity.url, scrape='true')
            if 'updated_time' not in scrape_r:
                raise _error.OpenGraphError("Error while updating OG story '{}'.".format(entity.title))

            if 'page_id' in opts and opts['page_id']:
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
