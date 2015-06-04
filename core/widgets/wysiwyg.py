"""WYSIWYG Widgets.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core import assetman
from pytsite.core.html import TextArea
from .abstract import AbstractWidget


class WYSIWYGWidget(AbstractWidget):

    def __init__(self, **kwargs: dict):
        """Init.
        """
        super().__init__(**kwargs)
        assetman.add_css('pytsite.core.widgets@ckeditor/skins/moono/editor.css')
        assetman.add_js('pytsite.core.widgets@ckeditor/ckeditor.js')
        assetman.add_js('pytsite.core.widgets@ckeditor/adapters/jquery.js')
        assetman.add_js('pytsite.core.widgets@wysiwyg.js')

    def render(self) -> str:
        """Render the widget.
        """
        text_area = TextArea(name=self._uid)
        return self._group_wrap(text_area, 'widget-wysiwyg')
