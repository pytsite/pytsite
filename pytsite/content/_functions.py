"""PytSite Content Package.
"""
import hashlib as _hashlib
import pytz as _pytz
from datetime import datetime as _datetime
from os import path as _path, makedirs as _makedirs
from pytsite import admin as _admin, taxonomy as _taxonomy, auth as _auth, odm as _odm, util as _util, \
    router as _router, lang as _lang, logger as _logger, feed as _feed, reg as _reg, settings as _settings
from . import _model

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


__models = {}


def register_model(model: str, cls, title: str, menu_weight: int=0, icon: str='fa fa-file-text-o', replace=False):
    """Register content model.
    """
    if isinstance(cls, str):
        cls = _util.get_class(cls)

    if not issubclass(cls, _model.Content):
        raise TypeError('Subclass of content model expected.')

    if not replace and is_model_registered(model):
        raise KeyError("Model '{}' is already registered.".format(model))

    # Register ODM model
    _odm.register_model(model, cls, replace)

    # Saving info about registered model
    __models[model] = (cls, title)

    # Register 'bypass_moderation' permission
    mock = _odm.dispense(model)
    perm_name = 'pytsite.content.bypass_moderation.' + model
    perm_description = mock.resolve_partly_msg_id('content_permission_bypass_moderation_' + model)
    _auth.define_permission(perm_name, perm_description, mock.package_name())

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


def create(model: str) -> _model.Content:
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

    f = _odm.find(model).sort([('publish_time', _odm.I_DESC)])

    if not language:
        language = _lang.get_current()
    f.where('language', '=', language)

    if status:
        f.where('status', '=', status)
    if check_publish_time:
        f.where('publish_time', '<=', _datetime.now())

    return f


def get_publish_statuses() -> list:
    """Get allowed content publication statuses.
    """
    r = []
    for s in ('published', 'waiting', 'unpublished'):
        r.append((s, _lang.t('pytsite.content@status_' + s)))

    return r


def get_sections(language: str=None) -> _odm.FinderResult:
    return list(_taxonomy.find('section', language).sort([('order', _odm.I_ASC)]).get())


def get_section(alias: str, language: str=None) -> _model.Section:
    return _taxonomy.find('section', language).where('alias', '=', alias).first()


def create_section(title: str, alias: str=None, language: str=None) -> _model.Section:
    return _taxonomy.dispense('section', title, alias, language).save()


def get_tags(limit: int=0, language: str=None) -> _odm.FinderResult:
    return _taxonomy.find('tag', language).get(limit)


def get_tag(alias: str, language: str=None) -> _model.Tag:
    return _taxonomy.find('tag', language).where('alias', '=', alias).first()


def create_tag(title: str, alias: str=None, language: str=None) -> _model.Tag:
    return _taxonomy.dispense('tag', title, alias, language).save()


def generate_feeds(model: str, filename: str, finder_adj=None, **kwargs):
    md5 = _hashlib.md5()
    content_settings = _settings.get_setting('content')
    length = kwargs.get('length', 20)
    language = kwargs.get('language', _lang.get_current())
    title = kwargs.get('title', content_settings.get('home_title_' + language))
    description = kwargs.get('description', content_settings.get('home_description_' + language))

    if not title:
        raise ValueError('Cannot set feed title. Please set it on the content settings form.')
    if not description:
        raise ValueError('Cannot set feed description. Please set it on the content settings form.')

    # Setup writer
    writer = _feed.Writer(title, _router.base_url(), description)

    # Setup finder
    finder = find(model, language=language)
    if finder_adj:
        finder_adj(finder)

    # Preparing output directory
    output_dir = _path.join(_reg.get('paths.static'), 'feed')
    if not _path.exists(output_dir):
        _makedirs(output_dir, 0o755, True)

    for entity in finder.get(length):
        entry = writer.add_entry()

        # Entry unique ID
        md5.update(entity.title.encode())
        entry.id(md5.hexdigest())

        # Entry title
        entry.title(entity.title)

        # Description
        entry.content(entity.description if entity.description else entity.title, type='text/plain')

        # Link
        entry.link({'href': entity.url})

        # Publish date
        tz = _pytz.timezone(_reg.get('server.timezone', 'UTC'))
        entry.pubdate(tz.localize(entity.publish_time))

        author_info = {'name': entity.author.full_name, 'email': entity.author.email}
        if entity.author.profile_is_public:
            author_info['uri'] = _router.ep_url('pytsite.auth_ui.ep.profile_view', {
                'nickname': str(entity.author.nickname),
            })
        entry.author(author_info)

        if entity.has_field('section'):
            entry.category({
                'term': entity.section.alias,
                'label': entity.section.title,
            })

        if entity.has_field('tags'):
            for tag in entity.tags:
                entry.category({
                    'term': tag.alias,
                    'label': tag.title,
                })

    # Write feed into files
    for out_type in 'rss', 'atom':
        out_path = _path.join(output_dir, '{}-{}.xml'.format(out_type, filename))

        if out_type == 'rss':
            writer.rss_file(out_path, True)
            _logger.info("RSS feed successfully written to '{}'.".format(out_path), __name__)

        if out_type == 'atom':
            writer.atom_file(out_path, True)
            _logger.info("Atom feed successfully written to '{}'.".format(out_path), __name__)
