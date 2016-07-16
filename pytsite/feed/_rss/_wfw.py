"""PytSite RSS Parser WFW Extensions.
"""
from typing import Tuple as _Tuple
from . import _em

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Comment(_em.NonEmptyUrl):
    @property
    def name(self):
        return '{http://wellformedweb.org/CommentAPI}comment'

    @property
    def valid_parents(self) -> _Tuple[str]:
        return 'item',


class CommentRss(_em.NonEmptyUrl):
    @property
    def name(self):
        return '{http://wellformedweb.org/CommentAPI}commentRss'

    @property
    def valid_parents(self) -> _Tuple[str]:
        return 'item',
