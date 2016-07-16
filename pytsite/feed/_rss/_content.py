"""PytSite RSS Parser Content Extensions.
"""
from . import _em

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Encoded(_em.Author):
    @property
    def name(self) -> str:
        return '{http://purl.org/rss/1.0/modules/content}encoded'
