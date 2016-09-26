"""PytSite RSS Parser.
"""
import requests as _requests
from datetime import datetime as _datetime
from lxml import etree as _etree
from pytsite import core_name as _core_name, core_version_str as _core_version_str, core_url as _core_url
from .. import _abstract, _xml, _error
from . import _em, _media, _pytsite, _dc, _sy, _content, _atom, _slash, _wfw, _yandex

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_tag_map = {
    'channel': _em.Channel,
    'title': _em.Title,
    'link': _em.Link,
    'comments': _em.Comments,
    'url': _em.Url,
    'guid': _em.Guid,
    'description': _em.Description,
    'generator': _em.Generator,
    'pubDate': _em.PubDate,
    'lastBuildDate': _em.LastBuildDate,
    'language': _em.Language,
    'item': _em.Item,
    'pdalink': _em.PdaLink,
    'author': _em.Author,
    'category': _em.Category,
    'enclosure': _em.Enclosure,
    'image': _em.Image,
    'width': _em.Width,
    'height': _em.Height,
    '{http://www.w3.org/2005/Atom}link': _atom.Link,
    '{http://purl.org/rss/1.0/modules/content}encoded': _content.Encoded,
    '{http://purl.org/rss/1.0/modules/syndication}updatePeriod': _sy.UpdatePeriod,
    '{http://purl.org/rss/1.0/modules/syndication}updateFrequency': _sy.UpdateFrequency,
    '{http://purl.org/rss/1.0/modules/slash}comments': _slash.Comments,
    '{http://purl.org/dc/elements/1.1}creator': _dc.Creator,
    '{http://search.yahoo.com/mrss}group': _media.Group,
    '{http://search.yahoo.com/mrss}player': _media.Player,
    '{http://wellformedweb.org/CommentAPI}comment': _wfw.Comment,
    '{http://wellformedweb.org/CommentAPI}commentRss': _wfw.CommentRss,
    '{https://pytsite.xyz}fullText': _pytsite.FullText,
    '{https://pytsite.xyz}tag': _pytsite.Tag,
    '{http://news.yandex.ru}logo': _yandex.Logo,
    '{http://news.yandex.ru}full-text': _yandex.FullText,
}


class Parser(_abstract.Parser, _xml.Serializable):
    """RSS Generator.
    """

    def __init__(self, skip_bad_elements: bool = True):
        """Init.
        """
        super().__init__(nsmap={
            'content': 'http://purl.org/rss/1.0/modules/content',
            'dc': 'http://purl.org/dc/elements/1.1',
            'media': 'http://search.yahoo.com/mrss',
            'sy': 'http://purl.org/rss/1.0/modules/syndication',
            'slash': 'http://purl.org/rss/1.0/modules/slash',
            'wfw': 'http://wellformedweb.org/CommentAPI',
            'pytsite': 'https://pytsite.xyz',
            'yandex': 'http://news.yandex.ru',
        })

        self._skip_bad_elements = skip_bad_elements

        self.append_child(_em.Channel())

    @property
    def name(self) -> str:
        return 'rss'

    @property
    def attributes(self) -> dict:
        return {
            'version': '2.0',
        }

    def load(self, source: str):
        def parse_xml_element(xml_em: _etree.Element) -> _xml.Serializable:
            # Remove trailing slash from namespace
            xml_tag_name = xml_em.tag.replace('/}', '}')

            # Check if we know how to handle an element
            if xml_tag_name not in _tag_map:
                raise _error.UnknownElement("Unknown RSS element: '{}'.".format(xml_em.tag))

            # Element itself
            em = _tag_map[xml_tag_name](xml_em.text, **dict(xml_em.items()))  # type: _xml.Serializable

            # Child elements
            for xml_child in xml_em:
                try:
                    em.append_child(parse_xml_element(xml_child))
                except (_error.UnknownElement, _error.ElementParsingError) as e:
                    if not self._skip_bad_elements:
                        raise e

            return em

        # Load remote data
        r = _requests.get(source, headers={
            'User-Agent': 'Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/31.0',
        })

        # Check response
        if not r.ok:
            raise _error.ReadError("HTTP error at {}. Code: {}. Reason: {}. Headers: {}. Content: {}".
                                   format(source, r.status_code, r.reason, r.headers, r.content))

        # Parse XML
        xml_root = _etree.fromstring(r.content)

        if xml_root.tag != 'rss':
            raise _error.ReadError("Cannot find <rss> root element at {}.".format(source))

        if not len(xml_root) or xml_root[0].tag != 'channel':
            raise _error.ReadError("Cannot find <channel> element at {}.".format(source))

        channel = self.get_children('channel')[0]
        for channel_xml_em in xml_root[0]:
            try:
                channel.append_child(parse_xml_element(channel_xml_em))
            except (_error.UnknownElement, _error.ElementParsingError) as e:
                if not self._skip_bad_elements:
                    raise e

    def generate(self) -> str:
        """Generate feed's XML string.
        """
        channel = self.get_children('channel')[0]
        if not channel.has_children('generator'):
            channel.append_child(_em.Generator('{}-{} ({})'.format(_core_name, _core_version_str(), _core_url)), 0)
            channel.append_child(_em.PubDate(_datetime.now()), 1)
            channel.append_child(_em.LastBuildDate(_datetime.now()), 2)

        return _etree.tostring(self.get_content(), encoding='UTF-8', xml_declaration=True, pretty_print=True).decode()
