"""PytSite RSS Parser Syndication Extensions.
"""
from typing import Tuple as _Tuple
from . import _em

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class UpdatePeriod(_em.NonEmpty):
    @property
    def name(self) -> str:
        return '{http://purl.org/rss/1.0/modules/syndication}updatePeriod'

    @property
    def valid_parents(self) -> _Tuple[str]:
        return 'channel'


class UpdateFrequency(_em.Integer):
    @property
    def name(self) -> str:
        return '{http://purl.org/rss/1.0/modules/syndication}updateFrequency'

    @property
    def valid_parents(self) -> _Tuple[str]:
        return 'channel'
