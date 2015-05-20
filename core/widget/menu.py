"""Menu Widget.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from .abstract import AbstractWidget


class MenuItemWidget(AbstractWidget):
    pass


class MenuWidget(AbstractWidget):
    def __init__(self, **kwargs: dict):
        """Init.
        """

        super().__init__(**kwargs)

        self._href = kwargs.get('href')
        self._icon = kwargs.get('icon')
        self._active = kwargs.get('active')

    def render(self):
        pass
