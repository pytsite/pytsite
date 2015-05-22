"""Wrapper Widget.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core.html import Div
from .abstract import AbstractWidget


class WrapperWidget(AbstractWidget):
    """Wrapper Widget.
    """

    def render(self) -> str:
        """Render the widget.
        """

        r = ''
        for child in self.children:
            r += child.render()

        return Div(r, cls=self.cls).render()
