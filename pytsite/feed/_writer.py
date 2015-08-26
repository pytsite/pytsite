"""Feed Writer.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import hashlib as _hashlib
from time import strftime as _strftime

from feedgen.feed import FeedGenerator as _FeedGenerator, FeedEntry as _FeedEntry

from pytsite import validation as _validation


class Writer:
    """Feed Writer.
    """
    def __init__(self, title: str, link: str, description: str):
        """Init.
        """
        v = _validation.rule.Url(value=link)
        if not v.validate():
            raise ValueError(v.message)

        self._generator = _FeedGenerator()
        self._generator.title(title)
        self._generator.link({'href': link})
        self._generator.description(description)
        self._generator.generator('PytSite')
        self._generator.lastBuildDate(_strftime('%Y-%m-%dT%H:%M%z'))

        md5 = _hashlib.md5()
        md5.update(link.encode())
        self._generator.id(md5.hexdigest())

    def add_entry(self) -> _FeedEntry:
        """Add a feed entry.
        """
        return self._generator.add_entry()

    def rss_str(self, pretty=True) -> str:
        """Generate RSS feed string.
        """
        return self._generator.rss_str(pretty)

    def atom_str(self, pretty=True) -> str:
        """Generate Atom feed string.
        """
        return self._generator.atom_str(pretty)

    def rss_file(self, path: str, pretty=False):
        """Generate RSS feed into file.
        """
        return self._generator.rss_file(path, pretty=pretty)

    def atom_file(self, path: str, pretty=False):
        """Generate Atom feed into file.
        """
        return self._generator.atom_file(path, pretty=pretty)
