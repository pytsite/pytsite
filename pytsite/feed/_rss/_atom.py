"""PytSite RSS Parser Atom Extensions.
"""
from typing import Tuple as _Tuple
from pytsite import validation as _validation
from . import _em

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Link(_em.Empty):
    def __init__(self, text: str = '', **kwargs):
        super().__init__(text, **kwargs)
        self._href = _validation.rule.Url(kwargs.get('href')).validate()
        self._rel = kwargs.get('rel', 'self')
        self._type = kwargs.get('type', 'text/html')

    @property
    def name(self) -> str:
        return '{http://www.w3.org/2005/Atom}link'

    @property
    def valid_parents(self) -> _Tuple[str]:
        return 'channel'

    @property
    def attributes(self) -> dict:
        return {
            'href': self._href,
            'rel': self._rel,
            'type': self._type,
        }
