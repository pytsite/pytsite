"""PytSite Content Import Drivers.
"""
from abc import ABC as _ABC, abstractmethod as _abstractmethod
from typing import Iterable as _Iterable
from frozendict import frozendict as _frozendict
from urllib.parse import urlparse
from pytsite import lang as _lang, widget as _widget, validation as _validation, feed as _feed, \
    content as _content, image as _image


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
        wrapper = _widget.Container(
            uid='driver_opts',
        )

        wrapper.add_widget(_widget.input.Text(
            uid='driver_opts[url]',
            label=_lang.t('pytsite.content_import@url'),
            value=driver_opts.get('url', ''),
            rules=_validation.rule.Url(),
            required=True,
        ))

        return wrapper

    def get_entities(self, options: _frozendict) -> _Iterable[_content.model.Content]:
        """Returns entities which should be imported.
        """
        o = options

        rss_reader = _feed.rss.Reader(o['url'])

        for rss_item in rss_reader.items:
            # Check for the images presence
            if o['with_images_only'] and not rss_item.enclosures:
                continue

            # Check for duplication
            f = _content.find(o['content_model'], status=None, check_publish_time=False)
            if f.where('ext_links', '=', rss_item.link).count():
                continue

            # Dispensing new entity
            entity = _content.dispense(o['content_model'])

            # Base entity's fields
            entity.f_set('author', o['content_author'])
            entity.f_set('status', o['content_status'])
            entity.f_set('language', o['content_language'])
            entity.f_set('title', rss_item.title)
            entity.f_set('publish_time', rss_item.pub_date)
            entity.f_set('description', rss_item.description)
            entity.f_set('body', rss_item.full_text)

            # Section
            if entity.has_field('section'):
                # Trying to find appropriate section
                for rss_category in rss_item.categories:
                    s = _content.find_section_by_title(rss_category.title, language=o['content_language'])
                    if s:
                        entity.f_set('section', s)
                        break

                # Set default section which has been chosen at the seetings form
                if not entity.section:
                    entity.f_set('section', o['content_section'])

            # Tags
            if entity.has_field('tags'):
                # Tags from RSS item
                for tag_title in rss_item.tags:
                    entity.f_add('tags', _content.dispense_tag(tag_title.title).save())

            # Images
            if entity.has_field('images') and rss_item.enclosures:
                for enc in rss_item.enclosures:
                    if enc.mime.startswith('image'):
                        entity.f_add('images', _image.create(enc.url))

            # Store information about content source
            entity.f_add('content_import', {
                'source_link': rss_item.link,
                'source_domain': urlparse(rss_item.link)[1]
            })
            if entity.has_field('ext_links'):
                entity.f_add('ext_links', rss_item.link)

            yield entity
