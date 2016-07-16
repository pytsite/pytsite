"""PytSite RSS Parser Yandex News Extensions.
"""
import re as _re
from . import _em

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


_full_text_re = (
    _re.compile('<img[^>]*>', _re.IGNORECASE),
    _re.compile('<iframe[^>]*>.*</iframe>', _re.IGNORECASE)
)


class Logo(_em.NonEmptyUrl):
    def __init__(self, url: str, **kwargs):
        """Init.
        """
        super().__init__(url, **kwargs)

        self._square = bool(kwargs.get('square'))

    @property
    def name(self) -> str:
        return '{http://news.yandex.ru}logo'

    @property
    def attributes(self) -> dict:
        return {'type': 'square'} if self._square else {}

    @property
    def valid_parents(self) -> tuple:
        return 'channel',


class FullText(_em.NonEmpty):
    def __init__(self, text: str, **kwargs):
        """Init.
        """
        for r in _full_text_re:
            text = r.sub('', text)

        super().__init__(text, **kwargs)

    @property
    def name(self):
        return '{http://news.yandex.ru}full-text'

    @property
    def valid_parents(self) -> tuple:
        return 'item',
