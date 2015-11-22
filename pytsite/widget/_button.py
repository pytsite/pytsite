"""Button Widgets.
"""
from pytsite import html as _html
from . import _base

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Button(_base.Base):
    """Button.
    """
    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        super().__init__(uid, **kwargs)

        self._icon = kwargs.get('icon')
        self._color = kwargs.get('color', 'default')
        self._css += ' btn btn-' + self._color

        self._html_em = _html.Button(uid=self._uid, type='button', cls=self.css)

    @property
    def icon(self) -> str:
        return self._icon

    @icon.setter
    def icon(self, value):
        self._icon = value

    def get_html_em(self) -> _html.Element:
        """Render the widget.
        """
        self._html_em.content = self.get_val()
        if self._icon and not self._html_em.children:
            self._html_em.append(_html.I(cls=self._icon))

        return self._html_em


class Submit(Button):
    """Submit Button.
    """
    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        super().__init__(uid, **kwargs)
        self._html_em = _html.Button(uid=self._uid, type='submit', cls=self._css)


class Link(Button):
    """Link Button.
    """
    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        super().__init__(uid, **kwargs)
        self._html_em = _html.A(uid=self._uid, href=kwargs.get('href', '#'), cls=self._css)

    @property
    def href(self) -> str:
        return self._html_em.get_attr('href')

    @href.setter
    def href(self, value: str):
        self._html_em.set_attr('href', value)
