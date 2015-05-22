"""Button Widgets.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core.html import Button as HtmlButton, I
from .abstract import AbstractWidget


class ButtonWidget(AbstractWidget):
    def __init__(self, **kwargs: dict):
        """Init.
        """

        super().__init__(**kwargs)
        self._icon = kwargs.get('icon')
        self._type = kwargs.get('type', 'button')
        self._color = kwargs.get('color', 'default')
        self._cls += 'btn btn-' + self._color

    def render(self) -> str:
        btn = HtmlButton(self.value, type=self.type, cls=self.cls)
        if self._icon:
            btn.append(I(cls=self._icon))

        return btn.render()

    @property
    def type(self):
        return self._type

    @property
    def icon(self):
        return self._icon


class SubmitButtonWidget(ButtonWidget):
    def __init__(self, **kwargs: dict):
        """Init.
        """

        super().__init__(**kwargs)
        self._type = 'submit'
