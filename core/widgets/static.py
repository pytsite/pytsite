"""Static Widgets.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core.html import P
from .abstract import AbstractWidget


class StaticTextWidget(AbstractWidget):
    """Static Text Widget.
    """

    def render(self) -> str:
        """Render the widget.
        """

        return self._group_wrap(P(self._value, cls='form-control-static'))
