"""Disqus Widgets.
"""
from pytsite import widget as _widget, html as _html, reg as _reg, tpl as _tpl

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Comments(_widget.Base):
    """Disqus Comments Widget.
    """
    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        super().__init__(uid, **kwargs)

        self._short_name = _reg.get('disqus.short_name')

    @property
    def short_name(self) -> str:
        """Get Disqus short name.
        """
        return self._short_name

    def get_html_em(self, **kwargs) -> _html.Element:
        """Render the widget.
        :param **kwargs:
        """
        return _html.Div(_tpl.render('pytsite.disqus@widget', {'widget': self}),
                         uid=self._uid, cls='widget widget-disqus')
