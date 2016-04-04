"""Content Export VK Driver.
"""
from frozendict import frozendict as _frozendict
import re as _re
from pytsite import content as _content, content_export as _content_export, logger as _logger, widget as _widget
from ._widget import Auth as _VKAuthWidget
from ._session import Session as _VKSession

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


_re_access_token = _re.compile('access_token=([0-9a-f]+)')
_re_user_id = _re.compile('user_id=(\d+)')


class Driver(_content_export.AbstractDriver):
    """Content Export Driver.
    """
    def get_name(self) -> str:
        """Get system name of the driver.
        """
        return 'vk'

    def get_description(self) -> str:
        """Get human readable description of the driver.
        """
        return 'pytsite.vk@vkontakte'

    def get_options_description(self, driver_options: _frozendict) -> str:
        """Get human readable driver options.
        """
        r = 'User ID: ' + str(self._parse_user_id(driver_options['access_url']))
        if driver_options['group_id'] != '0':
            r += ', Page ID: ' + driver_options['group_id']

        return r

    def get_settings_widget(self, driver_opts: _frozendict) -> _widget.Base:
        """Add widgets to the settings form of the driver.
        """
        return _VKAuthWidget(
            uid='driver_opts',
            access_url=driver_opts.get('access_url'),
            group_id=driver_opts.get('group_id'),
        )

    def export(self, entity: _content.model.Content, exporter=_content_export.model.ContentExport):
        """Export data.
        """
        _logger.info("Export started. '{}'".format(entity.title), __name__)

        opts = exporter.driver_opts  # type: _frozendict

        tags = ['#' + t for t in exporter.add_tags if ' ' not in t]
        tags += ['#' + t.title for t in entity.tags if ' ' not in t.title]
        message = '{} {} {}'.format(entity.title, ' '.join(tags), entity.url)

        try:
            owner_id = -int(opts['group_id']) if opts['group_id'] != '0' else self._parse_user_id(opts['access_url'])

            s = _VKSession(self._parse_access_token(opts['access_url']))
            if entity.images:
                r = s.wall_post(owner_id, message, entity.images[0], entity.url)
            else:
                r = s.wall_post(owner_id, message)

            _logger.info("Export finished. '{}'. VK response: {}".format(entity.title, r), __name__)

        except Exception as e:
            raise _content_export.error.ExportError(e)

    def _parse_user_id(self, access_url: str) -> int:
        try:
            return int(_re_user_id.findall(access_url)[0])
        except IndexError:
            return 0

    def _parse_access_token(self, access_url: str) -> str:
        return _re_access_token.findall(access_url)[0]
