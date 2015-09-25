"""Button Widgets.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import html as _html
from . import _base


class Button(_base.Base):
    """Button.
    """
    def __init__(self, **kwargs: dict):
        """Init.
        """
        super().__init__(**kwargs)
        self._icon = kwargs.get('icon')
        self._color = kwargs.get('color', 'default')
        self._css += ' btn btn-' + self._color

        self._em = _html.Button(uid=self._entity, type='button', cls=self.css)

    @property
    def icon(self) -> str:
        return self._icon

    @icon.setter
    def icon(self, value):
        self._icon = value

    def render(self) -> str:
        """Render the widget.
        """
        self._em.content = self.get_value()
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
        self._em = _html.Button(uid=self._entity, type='submit', cls=self._css)


class Link(Button):
    """Link Button.
    """
    def __init__(self, href: str, **kwargs: dict):
        """Init.
        """
        super().__init__(**kwargs)
        self._em = _html.A(uid=self._entity, href=href, cls=self._css)

    @property
    def href(self) -> str:
        return self._em.get_attr('href')

    @href.setter
    def href(self, value: str):
        self._em.set_attr('href', value)
