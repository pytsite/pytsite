"""WYSIWYG Widgets.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core import assetman, html
from ._abstract import Widget


class CKEditor(Widget):
    """CKEditor Widget.
    """
    def __init__(self, **kwargs: dict):
        """Init.
        """
        super().__init__(**kwargs)
        self._group_cls = ' '.join((self._group_cls, 'widget-ckeditor'))
        assetman.add('pytsite.core.widget@ckeditor/skins/moono/editor.css')
        assetman.add('pytsite.core.widget@ckeditor/ckeditor.js')
        assetman.add('pytsite.core.widget@ckeditor/adapters/jquery.js')
        assetman.add('pytsite.core.widget@js/ckeditor.js')

    def render(self) -> str:
        """Render the widget.
        """
        text_area = html.TextArea(name=self._uid)
        return self._group_wrap(text_area)
