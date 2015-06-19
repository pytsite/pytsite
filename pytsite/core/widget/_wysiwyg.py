"""WYSIWYG Widgets.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core import assetman as _assetman, html as _html
from . import _base


class CKEditor(_base.Widget):
    """CKEditor Widget.
    """
    def __init__(self, **kwargs: dict):
        """Init.
        """
        super().__init__(**kwargs)
        self._group_cls = ' '.join((self._group_cls, 'widget-ckeditor'))
        _assetman.add('pytsite.core.widget@ckeditor/skins/moono/editor.css')
        _assetman.add('pytsite.core.widget@ckeditor/ckeditor.js')
        _assetman.add('pytsite.core.widget@ckeditor/adapters/jquery.js')
        _assetman.add('pytsite.core.widget@js/ckeditor.js')

    def render(self) -> str:
        """Render the widget.
        """
        return self._group_wrap(_html.TextArea(name=self._uid))
