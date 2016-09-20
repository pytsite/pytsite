"""PytSite Content Import Drivers.
"""
from abc import ABC as _ABC, abstractmethod as _abstractmethod
from typing import Iterable as _Iterable, Tuple as _Tuple
from frozendict import frozendict as _frozendict
from urllib.parse import urlparse
from pytsite import lang as _lang, widget as _widget, validation as _validation, feed as _feed, util as _util, \
    content as _content, file as _file

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Abstract(_ABC):
    """Abstract Content Import Driver.
    """

    @_abstractmethod
    def get_name(self) -> str:
        """Get the system name of the driver.
        """
        pass

    @_abstractmethod
    def get_description(self) -> str:
        """Get the human readable description of the driver.
        """
        pass

    @_abstractmethod
    def get_settings_widget(self, driver_opts: _frozendict):
        """Add widgets to the settings form of the driver.
        """
        pass

    @_abstractmethod
    def get_entities(self, options: _frozendict) -> _Iterable[_content.model.Content]:
        pass


class RSS(Abstract):
    """RSS Content Import Driver.
    """

    def get_name(self) -> str:
        """Get name of the driver.
        """
        return 'rss'

    def get_description(self) -> str:
        """Get the human readable description of the driver.
        """
        return _lang.t('pytsite.content_import@rss')

    def get_settings_widget(self, driver_opts: _frozendict):
        """Add widgets to the settings form of the driver.
        """
        return _widget.input.Text(
            uid='driver_opts_url',
            label=_lang.t('pytsite.content_import@url'),
            value=driver_opts.get('url', ''),
            rules=_validation.rule.Url(),
            required=True,
        )

    def get_entities(self, options: _frozendict) -> _Iterable[_content.model.Content]:
        """Returns entities which should be imported.
        """
        o = options

        parser = _feed.rss.Parser()
        parser.load(o['url'])

        items = parser.get_children('channel')[0].get_children('item')  # type: _Tuple[_feed.rss.em.Element]
        for rss_item in items:
            # Check for duplication
            f = _content.find(o['content_model'], status=None, check_publish_time=False)
            if f.eq('ext_links', rss_item.get_children('link')[0].text).count():
                continue

            # Dispensing new entity
            entity = _content.dispense(o['content_model'])

            # Base entity's fields
            entity.f_set('author', o['content_author'])
            entity.f_set('status', o['content_status'])
            entity.f_set('language', o['content_language'])
            entity.f_set('title', rss_item.get_children('title')[0].text)
            entity.f_set('publish_time', _util.parse_rfc822_datetime_str(rss_item.get_children('pubDate')[0].text))

            # Description
            if rss_item.has_children('description'):
                entity.f_set('description', _util.strip_html_tags(rss_item.get_children('description')[0].text))

            # Section
            if entity.has_field('section') and rss_item.has_children('category'):
                # Trying to find appropriate section
                for category in rss_item.get_children('category'):
                    s = _content.find_section_by_title(category.text, language=o['content_language'])
                    if s:
                        entity.f_set('section', s)
                        break

                # Set default section which has been chosen at the settings form
                if not entity.section:
                    entity.f_set('section', o['content_section'])

            # Tags
            if entity.has_field('tags') and rss_item.has_children('{https://pytsite.xyz}tag'):
                for tag in rss_item.get_children('{https://pytsite.xyz}tag'):
                    tag_obj = _content.dispense_tag(tag.text.capitalize())
                    with tag_obj:
                        tag_obj.save()
                    entity.f_add('tags', tag_obj)

            # Video links
            if entity.has_field('video_links') and rss_item.has_children('{http://search.yahoo.com/mrss}group'):
                for m_group in rss_item.get_children('{http://search.yahoo.com/mrss}group'):
                    if m_group.has_children('{http://search.yahoo.com/mrss}player'):
                        m_player = m_group.get_children('{http://search.yahoo.com/mrss}player')[0]
                        entity.f_add('video_links', m_player.attributes['url'])

            # Body
            if entity.has_field('body'):
                body = None

                if rss_item.has_children('{https://pytsite.xyz}fullText'):
                    body = rss_item.get_children('{https://pytsite.xyz}fullText')[0].text
                elif rss_item.has_children('{http://purl.org/rss/1.0/modules/content}encoded'):
                    body = rss_item.get_children('{http://purl.org/rss/1.0/modules/content}encoded')[0].text
                elif rss_item.has_children('{http://news.yandex.ru}full-text'):
                    body = rss_item.get_children('{http://news.yandex.ru}full-text')[0].text

                if body:
                    entity.f_set('body', body)

            # Images from enclosures ONLY IF entity does not contain image links in the body
            if entity.has_field('images') and rss_item.has_children('enclosure') and '<img' not in entity.body:
                for enc in rss_item.get_children('enclosure'):
                    if enc.attributes['type'].startswith('image'):
                        entity.f_add('images', _file.create(enc.attributes['url']))

            # Store information about content source
            if rss_item.has_children('link'):
                rss_item_link = rss_item.get_children('link')[0].text
                entity.f_add('content_import', {
                    'source_link': rss_item_link,
                    'source_domain': urlparse(rss_item_link)[1]
                })
                if entity.has_field('ext_links'):
                    entity.f_add('ext_links', rss_item_link)

            yield entity
