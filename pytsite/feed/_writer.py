"""Feed Writer.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import hashlib as _hashlib
from feedgen.feed import FeedGenerator as _FeedGenerator, FeedEntry as _FeedEntry
from pytsite.core import validation as _validation


class Writer:
    def __init__(self, title: str, link: str, description: str):
        v = _validation.rule.Url(value=link)
        if not v.validate():
            raise ValueError(v.message)

        self.generator = _FeedGenerator()
        self.generator.title(title)
        self.generator.link({'href': link})
        self.generator.description(description)
        self.generator.generator('pytsite')

        md5 = _hashlib.md5()
        md5.update(link.encode())
        self.generator.id(md5.hexdigest())

    def add_entry(self) -> _FeedEntry:
        return self.generator.add_entry()

    def rss_str(self, pretty=True) -> str:
        return self.generator.rss_str(pretty)

    def atom_str(self, pretty=True) -> str:
        return self.generator.atom_str(pretty)

    def rss_file(self, path: str, pretty=False):
        return self.generator.rss_file(path, pretty=pretty)

    def atom_file(self, path: str, pretty=False):
        return self.generator.atom_file(path, pretty=pretty)
