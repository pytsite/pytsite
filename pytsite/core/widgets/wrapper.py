"""Wrapper Widget.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core.html import Div
from .abstract import AbstractWidget


class WrapperWidget(AbstractWidget):
    """Wrapper Widget.

    Can contain only children widgets.
    """

    def render(self) -> str:
        """Render the widget.
        """
        r = []
        for child in self.children:
            r.append(child.render())

        return Div(self._children_sep.join(r), cls=self.cls).render()
