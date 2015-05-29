"""Input Widgets.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core.html import Input as HtmlInput
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

        return HtmlInput(type='hidden', uid=self._uid, name=self.name, value=self.get_value()).render()


class TextInputWidget(InputWidget):
    """Text Input Widget
    """

    def __init__(self, **kwargs: dict):
        """Init.
        """

        super().__init__(**kwargs)
        self._cls = 'form-control'

    def render(self) -> str:
        """Render the widget
        """

        html_input = HtmlInput(
            type='text',
            uid=self._uid,
            name=self._name,
            value=self._value,
            cls=self._cls,
            placeholder=self.placeholder
        )

        return self._group_wrap(html_input.render())
