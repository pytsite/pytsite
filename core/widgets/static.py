"""Static Widgets.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core.html import P
from .abstract import AbstractWidget


class HtmlWidget(AbstractWidget):
    """HTML Widget.
    """

    def __init__(self, **kwargs: dict):
        """Init.
        """
        super().__init__(**kwargs)
        self._html_em = kwargs.get('html_em', P)

    def render(self) -> str:
        return self._html_em(self._value, cls=self._cls).render()


class StaticControlWidget(HtmlWidget):
    """Static Text Widget.
    """

    def render(self) -> str:
        """Render the widget.
        """
        return self._group_wrap(self._html_em(self._value, cls='form-control-static'))
