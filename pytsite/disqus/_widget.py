"""Disqus Widgets.
"""
from pytsite import widget as _widget, html as _html, reg as _reg, tpl as _tpl

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Disqus(_widget.Base):
    """Disqus Widget.
    """
    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        super().__init__(uid, **kwargs)

        short_name = _reg.get('disqus.short_name')
        if not short_name:
            raise ValueError("Configuration parameter 'disqus.short_name' is not defined.")

        self._short_name = short_name

    @property
    def short_name(self) -> str:
        """Get Disqus short name.
        """
        return self._short_name

    def get_html_em(self) -> _html.Element:
        """Render the widget.
        """
        return _html.Div(_tpl.render('pytsite.disqus@widget', {'widget': self}),
                         uid=self._uid, cls='widget widget-disqus')
