"""Hidden Input Widget
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core import html
from .input import InputWidget


class HiddenInputWidget(InputWidget):
    """Hidden Input Widget
    """

    def render(self) -> str:
        """Render the widget.
        """

        return html.Input(type='hidden', id=self.uid, name=self.name, value=self.value).render()
