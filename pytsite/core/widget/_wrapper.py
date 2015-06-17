"""Wrapper Widget.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core import html
from ._abstract import Widget


class Wrapper(Widget):
    """Wrapper Widget.

    Can contain only child widgets.
    """
    def render(self) -> str:
        """Render the widget.
        """
        r = []
        for child in self.children:
            r.append(child.render())

        return html.Div(self._children_sep.join(r), cls=self.cls).render()
