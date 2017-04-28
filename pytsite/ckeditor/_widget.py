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
        self._js_module = 'ckeditor'

    def _get_element(self, **kwargs) -> _html.Element:
        """Get HTML element of the widget.
        """
        return _html.TextArea(self.get_val(), name=self._uid)
