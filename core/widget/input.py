"""Input Widget.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core.html import Input as HtmlInputElement
from .abstract import AbstractWidget


class InputWidget(AbstractWidget):
    """Input Widget.
    """

    def render(self)->str:
        """Render the widget.
        """

        raise NotImplementedError()


class HiddenInputWidget(InputWidget):
    """Hidden Input Widget
    """

    def render(self) -> str:
        """Render the widget.
        """

        return HtmlInputElement(type='hidden', id=self.uid, name=self.name, value=self.value).render()


class TextInputWidget(InputWidget):
    """Text Input Widget
    """

    def render(self) -> str:
        """Render the widget
        """

        placeholder = 'placeholder="{}"'.format(self._placeholder) if self._placeholder else ''
        r = '<input type="text" id="{}" name="{}" {} value="{}">'.format(
            self.uid, self.name, placeholder, self.value)

        return self._group_wrap(r)
