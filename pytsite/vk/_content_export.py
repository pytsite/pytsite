"""Content Export VK Driver.
"""
from pytsite import content as _content, content_export as _content_export, widget as _widget, logger as _logger, \
    reg as _reg
from ._widget import Auth as _VKAuthWidget
from ._session import Session as _VKSession

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Driver(_content_export.AbstractDriver):
    """Content Export Driver.
    """
    def __init__(self, **kwargs):
        """Init.
        """
        self._app_id = _reg.get('vk.app_id')
        if not self._app_id:
            raise Exception("'vk.app_id' must be defined.")

        self._access_token = kwargs.get('access_token')
        self._user_id = int(kwargs.get('user_id', 0))
        self._group_id = int(kwargs.get('group_id', 0))

    def get_settings_widget(self, uid: str, **kwargs) -> _widget.Base:
        """Get widget for content export edit form.
        """
        return _VKAuthWidget(uid=uid, **kwargs)

    def export(self, entity: _content.model.Content, exporter=_content_export.model.ContentExport):
        """Export data.
        """
        _logger.info("Export started. '{}'".format(entity.title), __name__)

        tags = ['#' + t for t in exporter.add_tags if ' ' not in t]
        tags += ['#' + t.title for t in entity.tags if ' ' not in t.title]
        message = '{} {} {}'.format(entity.title, ' '.join(tags), entity.url)

        try:
            owner_id = -self._group_id if self._group_id else self._user_id

            s = _VKSession(self._access_token)
            if entity.images:
                r = s.wall_post(owner_id, message, entity.images[0], entity.url)
            else:
                r = s.wall_post(owner_id, message)

            _logger.info("Export finished. '{}'. VK response: {}".format(entity.title, r), __name__)
        except Exception as e:
            raise _content_export.error.ExportError(e)
