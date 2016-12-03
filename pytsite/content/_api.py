"""PytSite Content Package.
"""
from typing import Callable as _Callable, Iterable as _Iterable, List as _List
from datetime import datetime as _datetime
from urllib import parse as _urllib_parse
from os import path as _path, makedirs as _makedirs
from pytsite import admin as _admin, taxonomy as _taxonomy, odm as _odm, util as _util, settings as _settings, \
    router as _router, lang as _lang, logger as _logger, feed as _feed, reg as _reg, permissions as _permission, \
    route_alias as _route_alias, widget as _widget
from . import _model

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_models = {}


def register_model(model: str, cls, title: str, menu_weight: int = 0, icon: str = 'fa fa-file-text-o', replace=False):
    """Register content model.
    :type cls: str | _odm.model.Entity
    """
    # Resolve class
    if isinstance(cls, str):
        cls = _util.get_class(cls)  # type: _model.Base

    if not issubclass(cls, _model.Base):
        raise TypeError('Subclass of content model expected.')

    if not replace and is_model_registered(model):
        raise KeyError("Model '{}' is already registered.".format(model))

    # Register ODM model
    _odm.register_model(model, cls, replace)

    # Saving info about registered _content_ model
    _models[model] = (cls, title)

    perm_group = cls.odm_auth_permissions_group()
    mock = dispense(model)

    # Define 'bypass_moderation' permission
    if mock.has_field('status'):
        perm_name = 'pytsite.content.bypass_moderation.' + model
        perm_description = cls.resolve_msg_id('content_perm_bypass_moderation_' + model)
        _permission.define_permission(perm_name, perm_description, perm_group)

    # Define 'set_localization' permission
    if mock.has_field('localization_' + _lang.get_current()):
        perm_name = 'pytsite.content.set_localization.' + model
        perm_description = cls.resolve_msg_id('content_perm_set_localization_' + model)
        _permission.define_permission(perm_name, perm_description, perm_group)

    # Define 'set_date' permission
    if mock.has_field('publish_time'):
        perm_name = 'pytsite.content.set_publish_time.' + model
        perm_description = cls.resolve_msg_id('content_perm_set_publish_time_' + model)
        _permission.define_permission(perm_name, perm_description, perm_group)

    # Define 'set_starred' permission
    if mock.has_field('starred'):
        perm_name = 'pytsite.content.set_starred.' + model
        perm_description = cls.resolve_msg_id('content_perm_set_starred_' + model)
        _permission.define_permission(perm_name, perm_description, perm_group)

    _admin.sidebar.add_menu(
        sid='content',
        mid=model,
        title=title,
        href=_router.ep_path('pytsite.odm_ui@browse', {'model': model}),
        icon=icon,
        weight=menu_weight,
        permissions=(
            'pytsite.odm_perm.create.' + model,
            'pytsite.odm_perm.modify.' + model,
            'pytsite.odm_perm.modify_own.' + model,
            'pytsite.odm_perm.delete.' + model,
            'pytsite.odm_perm.delete_own.' + model,
        ),
        replace=replace
    )


def is_model_registered(model: str) -> bool:
    """Check if the content model is registered.
    """
    return model in _models


def get_models() -> dict:
    """Get registered content models.
    """
    return _models


def get_model(model: str) -> tuple:
    """Get model information.
    """
    if not is_model_registered(model):
        raise KeyError("Model '{}' is not registered as content model.".format(model))

    return _models[model]


def get_model_title(model: str) -> str:
    """Get human readable model title.
    """
    return _lang.t(get_model(model)[1])


def dispense(model: str, eid: str = None) -> _model.Content:
    """Create content entity.
    """
    if not is_model_registered(model):
        raise KeyError("Model '{}' is not registered as content model.".format(model))

    return _odm.dispense(model, eid)


def find(model: str, **kwargs):
    """Get content entities finder.
    """
    if not is_model_registered(model):
        raise KeyError("Model '{}' is not registered as content model.".format(model))

    f = _odm.find(model)

    # Publish time
    if f.mock.has_field('publish_time'):
        f.sort([('publish_time', _odm.I_DESC)])
        if kwargs.get('check_publish_time', True):
            f.cache(0)  # It is no sense to cache such queries because argument is different every time
            f.lte('publish_time', _datetime.now())
    else:
        f.sort([('_modified', _odm.I_DESC)])

    # Language
    if f.mock.has_field('language'):
        lng = kwargs.get('language')
        if not lng:
            f.eq('language', _lang.get_current())
        elif lng != '*':
            f.eq('language', lng)

    # Status
    if f.mock.has_field('status'):
        # DON'T change this construction!
        # Works same as with language above.
        if 'status' in kwargs:
            if kwargs['status'] is not None:
                f.eq('status', kwargs['status'])
        else:
            f.eq('status', 'published')

    return f


def find_by_url(url: str) -> _model.Content:
    parsed_url = _urllib_parse.urlsplit(url, allow_fragments=False)

    try:
        r_alias = _route_alias.get_by_alias(parsed_url[2])

        # Path should have format `/content/view/{model}/{id}`
        parsed_path = r_alias.target.split('/')
        if len(parsed_path) == 5:
            return dispense(parsed_path[3], parsed_path[4])
    except _route_alias.error.RouteAliasNotFound:
        pass


def get_statuses() -> _List[str]:
    """Get allowed content publication statuses.
    """
    r = []
    for s in ('published', 'waiting', 'unpublished'):
        r.append((s, _lang.t('pytsite.content@status_' + s)))

    return r


def get_sections(language: str = None) -> _Iterable[_model.Section]:
    """Get sections.
    """
    return _taxonomy.find('section', language).sort([('order', _odm.I_ASC)]).get()


def dispense_section(title: str, alias: str = None, language: str = None) -> _model.Section:
    """Get or create section.
    """
    return _taxonomy.dispense('section', title, alias, language)


def find_section_by_title(title: str, language: str = None) -> _model.Section:
    """Get section by title.
    """
    return _taxonomy.find_by_title('section', title, language)


def find_section_by_alias(alias: str, language: str = None) -> _model.Section:
    """Get section by title.
    """
    return _taxonomy.find_by_alias('section', alias, language)


def get_tags(limit: int = 0, language: str = None) -> _Iterable[_model.Tag]:
    """Get tags.
    """
    return _taxonomy.find('tag', language).sort([('weight', _odm.I_DESC)]).get(limit)


def dispense_tag(title: str, alias: str = None, language: str = None) -> _model.Tag:
    return _taxonomy.dispense('tag', title, alias, language)


def find_tag_by_title(title: str, language: str = None) -> _model.Tag:
    """Get tag by title.
    """
    return _taxonomy.find_by_title('tag', title, language)


def find_tag_by_alias(alias: str, language: str = None) -> _model.Tag:
    """Get tag by title.
    """
    return _taxonomy.find_by_alias('tag', alias, language)


def generate_rss(model: str, filename: str, lng: str = None, finder_setup: _Callable[[_odm.Finder], None] = None,
                 item_setup: _Callable[[_feed.xml.Serializable, _model.Content], None] = None, length: int = 20):
    """Generate RSS feeds.
    """
    if not lng:
        lng = _lang.get_current()

    # Setup finder
    finder = find(model, language=lng)
    if finder_setup:
        finder_setup(finder)

    # Preparing output directory
    output_dir = _path.join(_reg.get('paths.static'), 'feed')
    if not _path.exists(output_dir):
        _makedirs(output_dir, 0o755, True)

    # Create generator
    content_settings = _settings.get('content')
    parser = _feed.rss.Parser()

    # Get <channel> element
    channel = parser.get_children('channel')[0]

    # Channel title
    channel.append_child(_feed.rss.em.Title(content_settings.get('home_title_' + lng) or 'UNTITLED'))

    # Channel description
    channel.append_child(_feed.rss.em.Description(content_settings.get('home_description_' + lng)))

    # Channel link
    channel.append_child(_feed.rss.em.Link(_router.base_url()))

    # Channel language
    channel.append_child(_feed.rss.em.Language(lng))

    # Channel logo
    logo_url = _router.url(_reg.get('content.rss.logo_url', 'assets/app/img/logo-rss.png'))
    channel.append_child(_feed.rss.yandex.Logo(logo_url))
    square_logo_url = _router.url(_reg.get('content.rss.square_logo_url', 'assets/app/img/logo-rss-square.png'))
    channel.append_child(_feed.rss.yandex.Logo(square_logo_url, square=True))

    # Append channel's items
    for entity in finder.get(length):
        item = _feed.rss.em.Item()
        item.append_child(_feed.rss.em.Title(entity.title))
        item.append_child(_feed.rss.em.Link(entity.url))
        item.append_child(_feed.rss.em.PdaLink(entity.url))
        item.append_child(_feed.rss.em.Description(entity.description if entity.description else entity.title))
        item.append_child(_feed.rss.em.PubDate(entity.publish_time))
        item.append_child(_feed.rss.em.Author('{} ({})'.format(entity.author.email, entity.author.full_name)))

        # Section
        if entity.has_field('section'):
            item.append_child(_feed.rss.em.Category(entity.section.title))

        # Tags
        if entity.has_field('tags'):
            for tag in entity.tags:
                item.append_child(_feed.rss.pytsite.Tag(tag.title))

        # Images
        if entity.has_field('images') and entity.images:
            # Attaching all the images as enclosures
            for img in entity.images:
                item.append_child(_feed.rss.em.Enclosure(url=img.get_url(), length=img.length, type=img.mime))

        # Video links
        if entity.has_field('video_links') and entity.video_links:
            m_group = item.append_child(_feed.rss.media.Group())
            for link_url in entity.video_links:
                m_group.append_child(_feed.rss.media.Player(url=link_url))

        # Comments count
        if entity.has_field('comments_count'):
            item.append_child(_feed.rss.slash.Comments(entity.comments_count))

        # Body
        if entity.has_field('body'):
            item.append_child(_feed.rss.yandex.FullText(entity.f_get('body', process_tags=False, remove_tags=True)))
            item.append_child(_feed.rss.content.Encoded(entity.f_get('body', process_tags=False, remove_tags=True)))
            item.append_child(_feed.rss.pytsite.FullText(entity.f_get('body', process_tags=False)))

        if item_setup:
            item_setup(item, entity)

        channel.append_child(item)

    # Write feed content
    out_path = _path.join(output_dir, '{}-{}.xml'.format(filename, lng))
    with open(out_path, 'wt', encoding='utf-8') as f:
        f.write(parser.generate())

    _logger.info("RSS feed successfully written to '{}'.".format(out_path))


def paginate(finder: _odm.Finder, per_page: int = 10) -> dict:
    """Get paginated content finder query results.
    """
    pager = _widget.select.Pager('content-pager', total_items=finder.count(), per_page=per_page)

    entities = []
    for entity in finder.skip(pager.skip).get(pager.limit):
        if entity.check_permissions('view'):
            entities.append(entity)

    return {
        'entities': entities,
        'pager': pager,
    }
