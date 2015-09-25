"""Disqus Widgets.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import widget as _widget, html as _html, reg as _reg, tpl as _tpl


class Disqus(_widget.Base):
    """Disqus Widget.
    """
    def __init__(self, **kwargs):
        """Init.
        """
        super().__init__(**kwargs)
        short_name = _reg.get('disqus.short_name')
        if not short_name:
            raise ValueError("Configuration parameter 'disqus.short_name' is not defined.")

        self._short_name = short_name

    @property
    def short_name(self) -> str:
        """Get Disqus short name.
        """
        return self._short_name

    def render(self) -> _html.Element:
        """Render the widget.
        """
        return _html.Div(_tpl.render('pytsite.disqus@widget', {'widget': self}),
                         uid=self._entity, cls='widget widget-disqus')
