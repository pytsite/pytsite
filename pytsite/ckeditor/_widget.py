"""CKEditor Widget.
"""
from pytsite import html as _html, widget as _widget


__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class CKEditor(_widget.Abstract):
    """CKEditor Widget.
    """
    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        super().__init__(uid, **kwargs)

        self._css = ' '.join((self._css, 'widget-ckeditor'))

        self._assets.extend([
            'pytsite.ckeditor@ckeditor/skins/moono/editor.css',
            'pytsite.ckeditor@js/ckeditor_preconfig.js',
            'pytsite.ckeditor@ckeditor/ckeditor.min.js',
            'pytsite.ckeditor@ckeditor/adapters/jquery.js',
            'pytsite.ckeditor@js/ckeditor.js',
        ])

    def get_html_em(self, **kwargs) -> str:
        """Render the widget.
        :param **kwargs:
        """
        return self._group_wrap(_html.TextArea(self.get_val(), name=self._uid))
