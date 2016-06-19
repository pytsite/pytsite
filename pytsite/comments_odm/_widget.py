"""PytSite Native Comments Widget.
"""
from pytsite import widget as _pytsite_widget, html as _html

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Comments(_pytsite_widget.Base):
    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        super().__init__(uid, **kwargs)

        self._thread_id = kwargs.get('thread_id')
        if not self._thread_id:
            raise RuntimeError("Widget '{}': not thread_id was specified.".format(self.name))

        self._data['thread_id'] = self._thread_id

    def get_html_em(self, **kwargs):
        return _html.Div('comments here')
