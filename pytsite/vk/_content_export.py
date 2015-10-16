"""Content Export VK Driver.
"""
from pytsite import content as _content, content_export as _content_export, widget as _widget, logger as _logger, \
    reg as _reg
from ._widget import Auth as VKAuthWidget

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

    def get_widget(self, uid: str, **kwargs: dict) -> _widget.Base:
        """Get widget for content export edit form.
        """
        return VKAuthWidget(uid=uid, **kwargs)

    def export(self, entity: _content.model.Content, exporter=_content_export.model.ContentExport):
        """Export data.
        """
        _logger.info("Export started. '{}'".format(entity.title), __name__)
        _logger.info("Export finished. '{}'".format(entity.title), __name__)
