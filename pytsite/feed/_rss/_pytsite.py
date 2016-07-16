"""PytSite RSS Parser PytSite Extensions.
"""
from typing import Tuple as _Tuple
from . import _em

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Tag(_em.NonEmpty):
    @property
    def name(self):
        return '{https://pytsite.xyz}tag'

    @property
    def valid_parents(self) -> _Tuple[str]:
        return 'item',


class FullText(_em.NonEmpty):
    @property
    def name(self):
        return '{https://pytsite.xyz}fullText'

    @property
    def valid_parents(self) -> _Tuple[str]:
        return 'item',
