"""RSS Feed Elements
"""

import pytz as _pytz
from typing import Tuple as _Tuple
from time import tzname as _tzname
from datetime import datetime as _datetime
from lxml import etree as _etree
from pytsite import validation as _validation, util as _util
from .. import _xml, _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_tz = _pytz.timezone(_tzname[0])


class Element(_xml.Serializable):
    @property
    def name(self) -> str:
        raise NotImplementedError()


class Empty(Element):
    def __init__(self, text: str = '', **kwargs):
        # Empty elements does not accept content
        text = ''
        super().__init__(text, **kwargs)

    @property
    def name(self) -> str:
        raise NotImplementedError()


class Container(Empty):
    @property
    def name(self) -> str:
        raise NotImplementedError()


class NonEmpty(Element):
    def __init__(self, text: str = '', **kwargs):
        try:
            super().__init__(_validation.rule.NonEmpty(text).validate(), **kwargs)
        except _validation.error.RuleError:
            raise _error.ElementParsingError("Element '{}' must contain text data.".format(self.name))

    @property
    def name(self) -> str:
        raise NotImplementedError()


class Integer(Element):
    def __init__(self, text='', **kwargs):
        try:
            super().__init__(str(_validation.rule.Integer(text).validate()))
        except _validation.error.RuleError:
            raise _error.ElementParsingError("Element '{}' must contain integer data.".format(self.name))

    @property
    def name(self) -> str:
        raise NotImplementedError()


class Url(Element):
    def __init__(self, text: str = '', **kwargs):
        try:
            super().__init__(_validation.rule.Url(text).validate(), **kwargs)
        except _validation.error.RuleError:
            raise _error.ElementParsingError("Element '{}' must contain valid URL.".format(self.name))

    @property
    def name(self) -> str:
        return 'url'

    @property
    def valid_parents(self) -> _Tuple[str]:
        return 'image',


class NonEmptyUrl(NonEmpty, Url):
    @property
    def name(self) -> str:
        raise NotImplementedError()


class Date(NonEmpty):
    def __init__(self, date: _datetime, **kwargs):
        try:
            super().__init__(_util.rfc822_datetime_str(_validation.rule.DateTime(date).validate()), **kwargs)
        except _validation.error.RuleError:
            raise _error.ElementParsingError("Element '{}' must contain valid date.".format(self.name))

    @property
    def name(self) -> str:
        raise NotImplementedError()


class Channel(Container):
    @property
    def name(self) -> str:
        return 'channel'

    @property
    def valid_parents(self) -> _Tuple[str]:
        return 'rss',

    @property
    def required_children(self) -> _Tuple[str]:
        """Get tuple of required children for the element.
        """
        return 'title', 'link', 'description'


class Title(NonEmpty):
    @property
    def name(self) -> str:
        return 'title'

    @property
    def valid_parents(self) -> _Tuple[str]:
        return 'channel', 'item', 'image'


class Description(Element):
    @property
    def name(self) -> str:
        return 'description'

    @property
    def valid_parents(self) -> _Tuple[str]:
        return 'channel', 'item'


class Link(NonEmptyUrl):
    @property
    def name(self) -> str:
        return 'link'

    @property
    def valid_parents(self) -> _Tuple[str]:
        return 'channel', 'item', 'image'


class Comments(NonEmptyUrl):
    @property
    def name(self) -> str:
        return 'comments'

    @property
    def valid_parents(self) -> _Tuple[str]:
        return 'item',


class Guid(NonEmpty):
    def __init__(self, text: str = '', **kwargs):
        super().__init__(text, **kwargs)
        self._is_perma_link = kwargs.get('isPermaLink', 'false')

    @property
    def name(self) -> str:
        return 'guid'

    @property
    def attributes(self) -> dict:
        return {
            'isPermaLink': self._is_perma_link,
        }

    @property
    def valid_parents(self) -> _Tuple[str]:
        return 'item',


class PdaLink(Link):
    @property
    def name(self) -> str:
        return 'pdalink'


class Generator(NonEmpty):
    @property
    def name(self) -> str:
        return 'generator'

    @property
    def valid_parents(self) -> _Tuple[str]:
        return 'channel',


class Language(NonEmpty):
    @property
    def name(self) -> str:
        return 'language'

    @property
    def valid_parents(self) -> _Tuple[str]:
        return 'channel',


class PubDate(Date):
    @property
    def name(self) -> str:
        return 'pubDate'

    @property
    def valid_parents(self) -> _Tuple[str]:
        return 'channel', 'item'


class LastBuildDate(Date):
    @property
    def name(self) -> str:
        return 'lastBuildDate'

    @property
    def valid_parents(self) -> _Tuple[str]:
        return 'channel',


class Author(NonEmpty):
    @property
    def name(self) -> str:
        return 'author'

    @property
    def valid_parents(self) -> _Tuple[str]:
        return 'item',


class Enclosure(_xml.Serializable):
    def __init__(self, text: str = '', **kwargs):
        super().__init__()
        try:
            self._url = _validation.rule.NonEmpty(kwargs.get('url')).validate()
            self._url = _validation.rule.Url(self._url).validate()
        except _validation._error.RuleError:
            raise _error.ElementParsingError("Element '{}' has invalid 'url' attribute value.".format(self.name))

        try:
            self._length = str(kwargs.get('length', 0))
            self._type = _validation.rule.Regex(kwargs.get('type', 'text/html'), pattern='\w+/\w+').validate()
        except _validation._error.RuleError:
            raise _error.ElementParsingError("Element '{}' has invalid 'type' attribute value.".format(self.name))

    @property
    def name(self) -> str:
        return 'enclosure'

    @property
    def attributes(self) -> dict:
        return {
            'url': self._url,
            'length': self._length,
            'type': self._type,
        }

    @property
    def valid_parents(self) -> _Tuple[str]:
        return 'item',


class Category(_xml.Serializable):
    def __init__(self, title: str, domain: str = None):
        super().__init__()
        try:
            self._title = _validation.rule.NonEmpty(title).validate()
        except _validation.error.RuleError:
            raise _error.ElementParsingError('Category title cannot be empty.')

        try:
            self._domain = _validation.rule.Url(domain).validate()
        except _validation.error.RuleError:
            raise _error.ElementParsingError('Category domain must be an URL.')

    @property
    def name(self) -> str:
        return 'category'

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


class Item(_xml.Serializable):
    @property
    def name(self) -> str:
        return 'item'

    @property
    def valid_parents(self) -> _Tuple[str]:
        return 'channel',

    @property
    def required_children(self) -> _Tuple[str]:
        """Get tuple of required children for the element.
        """
        return 'title', 'link', 'pubDate'


class Image(Container):
    @property
    def name(self) -> str:
        return 'image'

    @property
    def valid_parents(self) -> _Tuple[str]:
        return 'channel',


class Width(Integer):
    @property
    def name(self) -> str:
        return 'width'

    @property
    def valid_parents(self) -> _Tuple[str]:
        return 'image',


class Height(Integer):
    @property
    def name(self) -> str:
        return 'height'

    @property
    def valid_parents(self) -> _Tuple[str]:
        return 'image',
