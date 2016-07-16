"""PytSite RSS Parser Media Extensions.
"""
from pytsite import validation as _validation
from . import _em

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Group(_em.Container):
    @property
    def name(self) -> str:
        return '{http://search.yahoo.com/mrss}group'


class Player(_em.Empty):
    def __init__(self, text: str = '', **kwargs):
        super().__init__()

        self._url = _validation.rule.Url(kwargs.get('url')).validate()
        self._width = kwargs.get('width')
        self._height = kwargs.get('height')

    @property
    def name(self) -> str:
        return '{http://search.yahoo.com/mrss}player'

    @property
    def attributes(self) -> dict:
        r = {'url': self._url}

        if self._width and self._height:
            r.update({
                'width': str(self._width),
                'height': str(self._height),
            })

        return r

    @property
    def valid_parents(self) -> tuple:
        return '{http://search.yahoo.com/mrss}group',
