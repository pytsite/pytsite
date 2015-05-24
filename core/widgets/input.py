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

    def __init__(self, **kwargs: dict):
        """Init.
        """

        super().__init__(**kwargs)
        self.cls = 'form-control'

    def render(self) -> str:
        """Render the widget
        """

        html_input = HtmlInputElement(
            type='text',
            id=self.uid,
            name=self.name,
            value=self.value,
            cls=self.cls,
            placeholder=self.placeholder
        )

        return self._group_wrap(html_input.render())
