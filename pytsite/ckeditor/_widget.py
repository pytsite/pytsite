"""CKEditor Widget.
"""
from pytsite import assetman as _assetman, html as _html, widget as _widget

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class CKEditor(_widget.Base):
    """CKEditor Widget.
    """
    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        super().__init__(uid, **kwargs)

        self._css = ' '.join((self._css, 'widget-ckeditor'))
        _assetman.add('pytsite.ckeditor@js/ckeditor_preconfig.js')
        _assetman.add('pytsite.ckeditor@ckeditor/skins/moono/editor.css')
        _assetman.add('pytsite.ckeditor@ckeditor/ckeditor.min.js')
        _assetman.add('pytsite.ckeditor@ckeditor/adapters/jquery.js')
        _assetman.add('pytsite.ckeditor@js/ckeditor.js')

    def get_html_em(self) -> str:
        """Render the widget.
        """
        return self._group_wrap(_html.TextArea(self.get_val(), name=self._uid))
