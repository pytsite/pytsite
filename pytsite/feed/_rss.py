"""RSS Writer.
"""
import pytz as _pytz
import requests as _requests
from typing import List as _List, Tuple as _Tuple
from time import tzname as _tzname
from datetime import datetime as _datetime
from lxml import etree as _etree
from pytsite import validation as _validation, core_version_str as _pytsite_ver, util as _util, lang as _lang
from . import _xml, _abstract, _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_tz = _pytz.timezone(_tzname[0])


class Enclosure(_abstract.Serializable):
    def __init__(self, url: str, length: int, mime: str):
        super().__init__()
        self._url = _validation.rule.NonEmpty(url).validate()
        self._url = _validation.rule.Url(url).validate()
        self._length = str(length)
        self._mime = _validation.rule.Regex(mime, pattern='\w+/\w+').validate()

    @property
    def url(self) -> str:
        return self._url

    @property
    def length(self) -> str:
        return self._length

    @property
    def mime(self) -> str:
        return self._mime

    def get_content(self) -> _etree.Element:
        return _etree.Element('enclosure', url=self._url, length=self._length, mime=self._mime)


class Category(_abstract.Serializable):
    def __init__(self, title: str, domain: str=None):
        super().__init__()
        try:
            self._title = _validation.rule.NonEmpty(title).validate()
        except _validation.error.RuleError:
            raise ValueError('Category title cannot be empty.')

        try:
            self._domain = _validation.rule.Url(domain).validate()
        except _validation.error.RuleError:
            raise ValueError('Category domain must be an URL.')

    @property
    def title(self) -> str:
        return self._title

    @property
    def domain(self) -> str:
        return self._domain

    def get_content(self):
        em = _etree.Element('category', domain=self._domain) if self._domain else _etree.Element('category')
        em.text = self._title

        return em


class Tag(_abstract.Serializable):
    def __init__(self, title: str):
        super().__init__()
        try:
            self._title = _validation.rule.NonEmpty(title).validate()
        except _validation.error.RuleError:
            raise ValueError('Category title cannot be empty.')

    @property
    def title(self) -> str:
        return self._title

    def get_content(self):
        em = _etree.Element('{https://pytsite.shepetko.com}tag')
        em.text = self._title

        return em


class Item(_xml.Item):
    def __init__(self, **kwargs):
        super().__init__()
        self._title = kwargs.get('title', '')
        self._link = kwargs.get('link', '')
        self._description = kwargs.get('description', '')
        self._full_text = kwargs.get('full_text', '')
        self._pub_date = _tz.localize(kwargs.get('pub_date', _datetime.now()))
        self._author = kwargs.get('author')

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str):
        self._title = _validation.rule.NonEmpty(value).validate()

    @property
    def link(self) -> str:
        return self._link

    @link.setter
    def link(self, value: str):
        self._link = _validation.rule.NonEmpty(value).validate()
        self._link = _validation.rule.Url(value).validate()

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str):
        self._description = value

    @property
    def full_text(self) -> str:
        return self._full_text

    @full_text.setter
    def full_text(self, value: str):
        self._full_text = value

    @property
    def pub_date(self) -> _datetime:
        return self._pub_date

    @pub_date.setter
    def pub_date(self, value: _datetime):
        if not value.tzinfo:
            value = _tz.localize(value)

        self._pub_date = value

    @property
    def author(self) -> str:
        return self._author

    @author.setter
    def author(self, value):
        self._author = value

    @property
    def categories(self) -> _List[Category]:
        return [i for i in self.children if i.get_content().tag == 'category']

    @property
    def tags(self) -> _List[Tag]:
        return [i for i in self.children if i.get_content().tag == '{https://pytsite.shepetko.com}tag']

    @property
    def enclosures(self) -> _List[Enclosure]:
        return [i for i in self.children if i.get_content().tag == 'enclosure']

    def get_content(self) -> _etree.Element:
        root = _etree.Element('item')

        if not self._title:
            raise _error.ElementRequired('Title is required.')

        title = _etree.SubElement(root, 'title')
        title.text = self._title

        if not self._link:
            raise _error.ElementRequired('Link is required.')
        link = _etree.SubElement(root, 'link')
        link.text = self._link

        pub_date = _etree.SubElement(root, 'pubDate')
        pub_date.text = _util.rfc822_datetime_str(self._pub_date)

        if self._description:
            description = _etree.SubElement(root, 'description')
            description.text = self._description

        if self._full_text:
            full_text = _etree.SubElement(root, '{https://pytsite.shepetko.com}full_text')
            full_text.text = self._full_text

        if self._author:
            author = _etree.SubElement(root, 'author')
            author.text = self._author

        for child in self._children:
            root.append(child.get_content())

        return root


class Generator(_xml.Generator):
    """Feed Writer.
    """
    def __init__(self, title: str, link: str, description: str, nsmap: dict=None, **kwargs):
        """Init.
        """
        if not nsmap:
            nsmap = {'pytsite': 'https://pytsite.shepetko.com'}
        else:
            nsmap.update({'pytsite': 'https://pytsite.shepetko.com'})

        super().__init__(nsmap)

        if not title:
            raise ValueError('RSS title cannot be empty.')
        if not link:
            raise ValueError('RSS link cannot be empty.')
        if not description:
            raise ValueError('RSS description cannot be empty.')

        try:
            _validation.rule.Url(link).validate()
        except _validation.error.RuleError:
            raise ValueError('RSS link must be a valid URL.')

        self._title = title
        self._link = link
        self._description = description
        self._generator = 'PytSite-' + _pytsite_ver()
        self._pub_date = kwargs.get('pub_date', _datetime.now())
        self._last_build_date = kwargs.get('build_date', _datetime.now())
        self._language = kwargs.get('language', _lang.get_current())

    def dispense_item(self, **kwargs) -> Item:
        """Dispense empty feed's item.
        """
        return Item(**kwargs)

    def get_xml_element(self) -> _etree.Element:
        """Generate RSS feed string.
        """
        rss = _etree.Element('rss', version='2.0', nsmap=self._nsmap)

        channel = _etree.SubElement(rss, 'channel')
        """:type: _etree.Element"""

        # Channel title
        channel_title = _etree.SubElement(channel, 'title')
        channel_title.text = self._title

        # Channel link
        channel_link = _etree.SubElement(channel, 'link')
        channel_link.text = self._link

        # Channel description
        channel_description = _etree.SubElement(channel, 'description')
        channel_description.text = self._description

        # Channel language
        channel_description = _etree.SubElement(channel, 'language')
        channel_description.text = self._language

        # Timestamps
        pub_date = _etree.SubElement(channel, 'pubDate')
        pub_date.text = _util.rfc822_datetime_str(self._pub_date)
        last_build_date = _etree.SubElement(channel, 'lastBuildDate')
        last_build_date.text = _util.rfc822_datetime_str(self._last_build_date)

        # Items
        for item in self.items:
            channel.append(item.get_content())

        return rss

    def generate(self) -> str:
        """Generate feed's XML string.
        """
        em = self.get_xml_element()

        return _etree.tostring(em, encoding='UTF-8', xml_declaration=True, pretty_print=True).decode()


class Reader(_xml.Reader):
    """RSS Feed Reader.
    """
    def __init__(self, source: str, autoload: bool=True):
        """Init.
        """
        super().__init__(source)

        self._xml = None  # type: _etree.Element

        self._title = ''
        self._link = ''
        self._description = ''
        self._language = ''
        self._pub_date = _datetime.now()
        self._last_build_date = _datetime.now()
        self._items = []  # type: _List[Item]

        if autoload:
            self.load()

    @property
    def title(self) -> str:
        return self._title

    @property
    def link(self) -> str:
        return self._link

    @property
    def description(self) -> str:
        return self._description

    @property
    def language(self) -> str:
        return self._language

    @property
    def pub_date(self) -> _datetime:
        return self._pub_date

    @property
    def last_build_date(self) -> _datetime:
        return self._last_build_date

    @property
    def items(self) -> _Tuple[Item]:
        return tuple(self._items)

    def load(self):
        r = _requests.get(self._source)
        if not r.ok:
            raise _error.ReadError("Cannot find valid RSS data at {}.".format(self._source))

        self._xml = _etree.fromstring(r.content)

        if self._xml.tag != 'rss':
            raise _error.ReadError("Cannot find <rss> root element at {}.".format(self._source))
        if self._xml[0].tag != 'channel':
            raise _error.ReadError("Cannot find <channel> element at {}.".format(self._source))

        for i in self._xml[0]:
            if i.tag == 'title':
                self._title = i.text
            elif i.tag == 'link':
                self._link = i.text
            elif i.tag == 'description':
                self._description = i.text
            elif i.tag == 'language':
                self._language = i.text
            elif i.tag == 'pubDate':
                self._pub_date = self._parse_date(i.text)
            elif i.tag == 'lastBuildDate':
                self._last_build_date = self._parse_date(i.text)
            elif i.tag == 'item':
                self._items.append(self._parse_item(i))

    def _parse_date(self, date_str: str) -> _datetime:
        return _util.parse_rfc822_datetime_str(date_str)

    def _parse_item(self, item_xml: _etree.Element) -> Item:
        item = Item()
        for i in item_xml:
            if i.tag == 'title':
                item.title = i.text
            elif i.tag == 'link':
                item.link = i.text
            elif i.tag == 'description':
                item.description = i.text
            elif i.tag.endswith('full_text') or i.tag.endswith('full-text'):
                item.full_text = i.text
            elif i.tag == 'author':
                item.author = i.text
            elif i.tag == 'pubDate':
                item.pub_date = self._parse_date(i.text)
            elif i.tag == 'category':
                item.append_child(Category(i.text, i.get('domain')))
            elif i.tag == '{https://pytsite.shepetko.com}tag':
                item.append_child(Tag(i.text))
            elif i.tag == 'enclosure':
                mime = i.get('mime') or i.get('type') or ''
                item.append_child(Enclosure(i.get('url'), i.get('length', 0), mime))

        return item
