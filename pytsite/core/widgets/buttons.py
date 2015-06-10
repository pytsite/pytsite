"""Button Widgets.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core.html import Button as HtmlButton, I, A
from .abstract import AbstractWidget


class ButtonWidget(AbstractWidget):
    """Button.
    """

    def __init__(self, **kwargs: dict):
        """Init.
        """

        super().__init__(**kwargs)
        self._icon = kwargs.get('icon')
        self._color = kwargs.get('color', 'default')
        self._cls += ' btn btn-' + self._color
        self._html_em = HtmlButton(self.get_value(), type='button')

    def render(self) -> str:
        """Render the widget.
        """
        self._html_em.set_attr('cls', self.cls)

        if self._icon:
            self._html_em.append(I(cls=self._icon))

        return self._html_em.render()


class SubmitButtonWidget(ButtonWidget):
    """Submit Button.
    """

    def __init__(self, **kwargs: dict):
        """Init.
        """
        super().__init__(**kwargs)
        self._html_em = HtmlButton(self.get_value(), uid=self._uid, type='submit')


class LinkButtonWidget(ButtonWidget):
    """Link Button.
    """

    def __init__(self, **kwargs: dict):
        """Init.
        """
        super().__init__(**kwargs)
        self._href = kwargs.get('href', '#')
        self._html_em = A(self.get_value(), uid=self._uid, href=self._href)

    @property
    def href(self) -> str:
        return self._href

    @href.setter
    def href(self, value: str):
        self._html_em.set_attr('href', value)
