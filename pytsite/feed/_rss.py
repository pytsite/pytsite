"""RSS Writer.
"""
import pytz as _pytz
from time import tzname as _tzname
from datetime import datetime as _datetime
from lxml import etree as _etree
from pytsite import validation as _validation, version_str as _pytsite_ver, util as _util
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

    def get_content(self) -> _etree.Element:
        return _etree.Element('enclosure', url=self._url, length=self._length, mime=self._mime)


class Category(_abstract.Serializable):
    def __init__(self, title: str, domain: str=None):
        super().__init__()
        self._title = _validation.rule.NonEmpty(title).validate()
        self._domain = _validation.rule.Url(domain).validate()

    def get_content(self):
        em = _etree.Element('category', domain=self._domain) if self._domain else _etree.Element('category')
        em.text = self._title

        return em


class Item(_xml.Item):
    def __init__(self, **kwargs):
        super().__init__()
        self._title = kwargs.get('title')
        self._link = kwargs.get('link')
        self._description = kwargs.get('description')
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
        self._description = _validation.rule.NonEmpty(value).validate()

    @property
    def pub_date(self) -> _datetime:
        return self._pub_date

    @pub_date.setter
    def pub_date(self, value: _datetime):
        self._pub_date = _tz.localize(value)

    @property
    def author(self) -> str:
        return self._author

    @author.setter
    def author(self, value):
        self._author = value

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
        pub_date.text = _util.rfc822_datetime(self._pub_date)

        if self._description:
            description = _etree.SubElement(root, 'description')
            description.text = self._description

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
        super().__init__(nsmap)
        self._title = _validation.rule.NonEmpty(title).validate()
        self._link = _validation.rule.NonEmpty(link).validate()
        self._link = _validation.rule.Url(link).validate()
        self._description = _validation.rule.NonEmpty(description).validate()
        self._generator = 'PytSite-' + _pytsite_ver()
        self._pub_date = _tz.localize(kwargs.get('pub_date', _datetime.now()))
        self._last_build_date = _tz.localize(kwargs.get('build_date', _datetime.now()))

    def dispense_item(self, **kwargs) -> Item:
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

        # Timestamps
        pub_date = _etree.SubElement(channel, 'pubDate')
        pub_date.text = _util.rfc822_datetime(self._pub_date)
        last_build_date = _etree.SubElement(channel, 'lastBuildDate')
        last_build_date.text = _util.rfc822_datetime(self._last_build_date)

        # Items
        for item in self.items:
            channel.append(item.get_content())

        return rss

    def generate(self) -> str:
        em = self.get_xml_element()
        return _etree.tostring(em, encoding='UTF-8', xml_declaration=True, pretty_print=True).decode()
