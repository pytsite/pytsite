"""PytSite Content Package.
"""
from typing import Callable as _Callable, Iterable as _Iterable, List as _List
from datetime import datetime as _datetime
from os import path as _path, makedirs as _makedirs
from pytsite import admin as _admin, taxonomy as _taxonomy, odm as _odm, util as _util, \
    router as _router, lang as _lang, logger as _logger, feed as _feed, reg as _reg, permission as _permission
from . import _model

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


__models = {}


def register_model(model: str, cls, title: str, menu_weight: int=0, icon: str='fa fa-file-text-o', replace=False):
    """Register content model.
    :type cls: str | _odm.Entity
    """
    # Resolve class
    if isinstance(cls, str):
        cls = _util.get_class(cls)

    if not issubclass(cls, _model.Base):
        raise TypeError('Subclass of content model expected.')

    if not replace and is_model_registered(model):
        raise KeyError("Model '{}' is already registered.".format(model))

    # Register ODM model
    _odm.register_model(model, cls, replace)

    # Saving info about registered _content_ model
    __models[model] = (cls, title)

    mock = dispense(model)

    # Define 'bypass_moderation' permission
    if mock.has_field('status'):
        perm_name = 'pytsite.content.bypass_moderation.' + model
        perm_description = cls.resolve_partly_msg_id('content_permission_bypass_moderation_' + model)
        _permission.define_permission(perm_name, perm_description, cls.package_name())

    # Define 'set_localization' permission
    if mock.has_field('localization_' + _lang.get_current()):
        perm_name = 'pytsite.content.set_localization.' + model
        perm_description = cls.resolve_partly_msg_id('content_permission_set_localization_' + model)
        _permission.define_permission(perm_name, perm_description, cls.package_name())

    # Define 'set_date' permission
    if mock.has_field('publish_time'):
        perm_name = 'pytsite.content.set_publish_time.' + model
        perm_description = cls.resolve_partly_msg_id('content_permission_set_publish_time_' + model)
        _permission.define_permission(perm_name, perm_description, cls.package_name())

    # Define 'set_starred' permission
    if mock.has_field('starred'):
        perm_name = 'pytsite.content.set_starred.' + model
        perm_description = cls.resolve_partly_msg_id('content_permission_set_starred_' + model)
        _permission.define_permission(perm_name, perm_description, cls.package_name())

    _admin.sidebar.add_menu(
        sid='content',
        mid=model,
        title=title,
        href=_router.ep_url('pytsite.odm_ui.ep.browse', {'model': model}),
        icon=icon,
        weight=menu_weight,
        permissions=(
            'pytsite.odm_ui.browse.' + model,
            'pytsite.odm_ui.browse_own.' + model,
        ),
        replace=replace
    )


def is_model_registered(model: str) -> bool:
    """Check if the content model is registered.
    """
    return model in __models


def get_models() -> dict:
    """Get registered content models.
    """
    return __models


def get_model(model: str) -> tuple:
    """Get model information.
    """
    if not is_model_registered(model):
        raise KeyError("Model '{}' is not registered as content model.".format(model))

    return __models[model]


def get_model_title(model: str) -> str:
    """Get human readable model title.
    """
    return _lang.t(get_model(model)[1])


def dispense(model: str) -> _model.Content:
    """Create content entity.
    """
    if not is_model_registered(model):
        raise KeyError("Model '{}' is not registered as content model.".format(model))

    return _odm.dispense(model)


def find(model: str, status='published', check_publish_time=True, language: str=None):
    """Get content entities finder.
    """
    if not is_model_registered(model):
        raise KeyError("Model '{}' is not registered as content model.".format(model))

    mock = dispense(model)
    f = _odm.find(model)

    if mock.has_field('publish_time'):
        f.sort([('publish_time', _odm.I_DESC)])
        if check_publish_time:
            f.cache(0)  # It has no sense to cache such queries because argument is different every time
            f.where('publish_time', '<=', _datetime.now())
    else:
        f.sort([('_modified', _odm.I_DESC)])

    if not language:
        language = _lang.get_current()
    f.where('language', '=', language)

    if status and mock.has_field('status'):
        f.where('status', '=', status)

    return f


def get_statuses() -> _List[str]:
    """Get allowed content publication statuses.
    """
    r = []
    for s in ('published', 'waiting', 'unpublished'):
        r.append((s, _lang.t('pytsite.content@status_' + s)))

    return r


def get_sections(language: str=None) -> _Iterable[_model.Section]:
    """Get sections.
    """
    return _taxonomy.find('section', language).sort([('order', _odm.I_ASC)]).get()


def dispense_section(title: str, alias: str=None, language: str=None) -> _model.Section:
    """Get or create section.
    """
    return _taxonomy.dispense('section', title, alias, language)


def find_section_by_title(title: str, language: str=None) -> _model.Section:
    """Get section by title.
    """
    return _taxonomy.find_by_title('section', title, language)


def find_section_by_alias(alias: str, language: str=None) -> _model.Section:
    """Get section by title.
    """
    return _taxonomy.find_by_alias('section', alias, language)


def get_tags(limit: int=0, language: str=None) ->  _Iterable[_model.Tag]:
    """Get tags.
    """
    return _taxonomy.find('tag', language).sort([('weight', _odm.I_DESC)]).get(limit)


def dispense_tag(title: str, alias: str=None, language: str=None) -> _model.Tag:
    return _taxonomy.dispense('tag', title, alias, language)


def find_tag_by_title(title: str, language: str=None) -> _model.Tag:
    """Get tag by title.
    """
    return _taxonomy.find_by_title('tag', title, language)


def find_tag_by_alias(alias: str, language: str=None) -> _model.Tag:
    """Get tag by title.
    """
    return _taxonomy.find_by_alias('tag', alias, language)


def generate_rss(generator: _feed.rss.Generator, model: str, filename: str, lng: str=None,
                 finder_setup: _Callable[[_odm.Finder], None]=None,
                 item_setup: _Callable[[_feed.rss.Item, _model.Content], None]=None,
                 length: int=20):
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

    for entity in finder.get(length):
        item = generator.dispense_item()
        item.title = entity.title
        item.link = entity.url
        item.description = entity.description if entity.description else entity.title
        item.full_text = entity.f_get('body', process_tags=False)
        item.pub_date = entity.publish_time
        item.author = '{} ({})'.format(entity.author.email, entity.author.full_name)

        # Category
        if entity.has_field('section'):
            item.append_child(_feed.rss.Category(entity.section.title))
        elif entity.has_field('tags'):
            item.append_child(_feed.rss.Category(entity.tags[0].title))

        # Tags
        if entity.has_field('tags'):
            for tag in entity.tags:
                item.append_child(_feed.rss.Tag(tag.title))

        if entity.has_field('images') and entity.images:
            # Attaching all the images as enclosures
            for img in entity.images:
                item.append_child(_feed.rss.Enclosure(img.url, img.length, img.mime))

        if item_setup:
            item_setup(item, entity)

        generator.append_item(item)

    # Write feed content
    out_path = _path.join(output_dir, '{}-{}.xml'.format(filename, lng))
    with open(out_path, 'wt', encoding='utf-8') as f:
        f.write(generator.generate())

    _logger.info("RSS feed successfully written to '{}'.".format(out_path), __name__)
