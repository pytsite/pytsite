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

        self._em = _html.Button(self.get_value(), uid=self._uid, type='button', cls=self.cls)

    def render(self) -> str:
        """Render the widget.
        """
        if self._icon and not self._em.children:
            self._em.append(_html.I(cls=self._icon))
        return self._em.render()


class Submit(Button):
    """Submit Button.
    """
    def __init__(self, **kwargs: dict):
        """Init.
        """
        super().__init__(**kwargs)
        self._em = _html.Button(self.get_value(), uid=self._uid, type='submit', cls=self._cls)


class Link(Button):
    """Link Button.
    """
    def __init__(self, href: str, **kwargs: dict):
        """Init.
        """
        super().__init__(**kwargs)
        self._em = _html.A(self.get_value(), uid=self._uid, href=href, cls=self._cls)

    @property
    def href(self) -> str:
        return self._em.get_attr('href')

    @href.setter
    def href(self, value: str):
        self._em.set_attr('href', value)
