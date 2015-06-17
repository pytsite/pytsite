"""Button Widgets.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core import html as _html
from . import _base


class Button(_base.Widget):
    """Button.
    """
    def __init__(self, **kwargs: dict):
        """Init.
        """
        super().__init__(**kwargs)
        self._icon = kwargs.get('icon')
        self._color = kwargs.get('color', 'default')
        self._cls += ' btn btn-' + self._color
        self._html_em = _html.Button(self.get_value(), type='button')

    def render(self) -> str:
        """Render the widget.
        """
        self._html_em.set_attr('cls', self.cls)

        if self._icon:
            self._html_em.append(_html.I(cls=self._icon))

        return self._html_em.render()


class Submit(Button):
    """Submit Button.
    """
    def __init__(self, **kwargs: dict):
        """Init.
        """
        super().__init__(**kwargs)
        self._html_em = _html.Button(self.get_value(), uid=self._uid, type='submit')


class Link(Button):
    """Link Button.
    """
    def __init__(self, **kwargs: dict):
        """Init.
        """
        super().__init__(**kwargs)
        self._href = kwargs.get('href', '#')
        self._html_em = _html.A(self.get_value(), uid=self._uid, href=self._href)

    @property
    def href(self) -> str:
        return self._href

    @href.setter
    def href(self, value: str):
        self._html_em.set_attr('href', value)
