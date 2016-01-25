"""RSS Feed Generator for Yandex.News.
"""
import re as _re
from lxml import etree as _etree
from pytsite import validation as _validation
from . import _abstract, _rss, _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


_full_text_re = (
    _re.compile('<img[^>]*>', _re.IGNORECASE),
    _re.compile('<iframe[^>]*>.*</iframe>', _re.IGNORECASE)
)


class Logo(_abstract.Serializable):
    def __init__(self, url: str, square=False):
        super().__init__()
        self._url = _validation.rule.NonEmpty(url).validate()
        self._url = _validation.rule.Url(url).validate()
        self._square = square

    def get_content(self) -> _etree.Element:
        em = _etree.Element('{http://news.yandex.ru}logo', type='square') if self._square \
            else _etree.Element('{http://news.yandex.ru}logo')
        em.text = self._url

        return em


class Item(_rss.Item):
    def __init__(self,  **kwargs):
        super().__init__(**kwargs)
        self._pdalink = kwargs.get('pdalink')

    @property
    def pdalink(self) -> str:
        return self._pdalink

    @pdalink.setter
    def pdalink(self, value: str):
        self._pdalink = value

    def get_content(self):
        content = super().get_content()

        if not self._full_text:
            raise _error.ElementRequired('Full text is required.')

        for re in _full_text_re:
            self.full_text = re.sub('', self._full_text)
        full_text = _etree.SubElement(content, '{http://news.yandex.ru}full-text')
        full_text.text = self._full_text

        if self._pdalink:
            pdalink = _etree.SubElement(content, 'pdalink')
            pdalink.text = _validation.rule.Url(self._pdalink).validate()

        return content


class Generator(_rss.Generator):
    def __init__(self, title: str, link: str, description: str, logo: str, logo_square: str):
        nsmap = {
            'yandex': 'http://news.yandex.ru',
            'media': 'http://search.yahoo.com/mrss'
        }

        self._logo = (Logo(logo), Logo(logo_square, square=True))
        """:type tuple[Logo]"""

        super().__init__(title, link, description, nsmap)

    def dispense_item(self, **kwargs) -> Item:
        return Item(**kwargs)

    def get_xml_element(self) -> _etree.Element:
        em = super().get_xml_element()

        # Insert yandex:logo after lastBuildDate
        for logo in self._logo:
            em[0].insert(5, logo.get_content())

        return em
