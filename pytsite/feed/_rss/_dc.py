"""PytSite RSS Parser Dublin Core Extensions.
"""
from typing import Tuple as _Tuple
from . import _em

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Creator(_em.NonEmpty):
    @property
    def name(self) -> str:
        return '{http://purl.org/dc/elements/1.1}creator'

    @property
    def valid_parents(self) -> _Tuple[str]:
        return 'item'
