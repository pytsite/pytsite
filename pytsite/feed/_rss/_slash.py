"""PytSite RSS Parser Slash Extensions.
"""
from typing import Tuple as _Tuple
from . import _em

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Comments(_em.Integer):
    @property
    def name(self):
        return '{http://purl.org/rss/1.0/modules/slash}comments'

    @property
    def valid_parents(self) -> _Tuple[str]:
        return 'item',
