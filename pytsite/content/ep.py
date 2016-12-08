"""Pytsite Content Endpoints.
"""
from datetime import datetime as _datetime
from pytsite import taxonomy as _taxonomy, odm_ui as _odm_ui, auth as _auth, http as _http, \
    router as _router, metatag as _metatag, assetman as _assetman, odm as _odm,  lang as _lang, tpl as _tpl, \
    logger as _logger, hreflang as _hreflang, comments as _comments
from . import _widget as _content_widget

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def index(args: dict, inp: dict):
    """Content Index.
    """
    # Delayed import to prevent circular dependency
    from . import _api

    # Checking if the model is registered
    model = args.get('model')
    if not model or not _api.is_model_registered(model):
        _logger.warn("Content model '{}' is not found. Redirecting to home.".format(model))
        return _http.response.Redirect(_router.base_url())

    # Getting finder
    f = _api.find(model)
    args['finder'] = f

    # Filter by term
    term_field = args.get('term_field')
    if term_field and f.mock.has_field(term_field):
        term_model = f.mock.get_field(term_field).model
        term_alias = args.get('term_alias')
        if term_alias and term_model != '*':
            term = _taxonomy.find(term_model).eq('alias', term_alias).first()
            if term:
                args['term'] = term
                if isinstance(f.mock.fields[term_field], _odm.field.Ref):
                    f.eq(term_field, term)
                elif isinstance(f.mock.fields[term_field], _odm.field.RefsList):
                    f.inc(term_field, term)
                _metatag.t_set('title', term.title)
            else:
                raise _http.error.NotFound()
        else:
            raise _http.error.NotFound()

    # Filter by author
    author_nickname = inp.get('author') or args.get('author')
    if author_nickname:
        author = _auth.get_user(nickname=author_nickname)

        if author:
            _metatag.t_set('title', _lang.t('pytsite.content@articles_of_author', {'name': author.full_name}))
            f.eq('author', author.uid)
            args['author'] = author
        else:
            raise _http.error.NotFound()

    # Search
    if inp.get('search'):
        query = inp.get('search')
        f.where_text(query)
        _metatag.t_set('title', _lang.t('pytsite.content@search', {'query': query}))

    return _router.call_ep('$theme@content_' + model + '_index', args, inp)


def view(args: dict, inp: dict):
    """View Content Entity.
    """
    from . import _api

    model = args.get('model')

    entity = _api.find(model, status=None, check_publish_time=False).eq('_id', args.get('id')).first()
    """:type: pytsite.content._model.Content"""

    # Check entity existence
    if not entity:
        raise _http.error.NotFound()

    # Check permissions
    if not entity.check_permissions('view'):
        raise _http.error.Forbidden()

    # Show non published entities only to users who can edit them
    if entity.has_field('publish_time') and entity.publish_time > _datetime.now():
        if not entity.check_permissions('modify'):
            raise _http.error.NotFound()
    if entity.has_field('status') and entity.status != 'published':
        if not entity.check_permissions('modify'):
            raise _http.error.NotFound()

    with entity:
        # Update entity's comments count
        _auth.switch_user_to_system()
        entity.f_set('comments_count', _comments.get_all_comments_count(entity.route_alias.alias)).save()
        _auth.restore_user()

    # Meta title
    if entity.has_field('title'):
        title = entity.title
        _metatag.t_set('title', title)
        _metatag.t_set('og:title', title)
        _metatag.t_set('twitter:title', title)

    # Meta description
    if entity.has_field('description'):
        description = entity.description
        _metatag.t_set('description', description)
        _metatag.t_set('og:description', description)
        _metatag.t_set('twitter:description', description)

    # Meta keywords
    if entity.has_field('tags'):
        _metatag.t_set('keywords', entity.f_get('tags', as_string=True))

    # Meta image
    if entity.has_field('images') and entity.images:
        _metatag.t_set('twitter:card', 'summary_large_image')
        image_w = 900
        image_h = 500
        image_url = entity.images[0].get_url(width=image_w, height=image_h)
        _metatag.t_set('og:image', image_url)
        _metatag.t_set('og:image:width', str(image_w))
        _metatag.t_set('og:image:height', str(image_h))
        _metatag.t_set('twitter:image', image_url)
    else:
        _metatag.t_set('twitter:card', 'summary')

    # Other metatags
    _metatag.t_set('og:type', 'article')
    _metatag.t_set('og:url', entity.url)
    _metatag.t_set('article:publisher', entity.url)

    if entity.has_field('author') and entity.author:
        _metatag.t_set('author', entity.author.full_name)
        _metatag.t_set('article:author', entity.author.full_name)

    # Alternate languages URLs
    for lng in _lang.langs(False):
        f_name = 'localization_' + lng
        if entity.has_field(f_name) and entity.f_get(f_name):
            _hreflang.add(lng, entity.f_get(f_name).url)

    _assetman.add('pytsite.content@js/content.js')

    args.update({
        'entity': entity,
        'entity_tag_cloud': _content_widget.EntityTagCloud('entity-tag-cloud', entity=entity)
    })

    return _router.call_ep('$theme@content_' + model + '_view', args, inp)


def modify(args: dict, inp: dict) -> str:
    """Get content entity create/modify form.
    """
    model = args['model']
    eid = args['id']

    try:
        frm = _odm_ui.get_m_form(model, eid if eid != 0 else None)

        if _router.is_ep_callable('$theme@content_' + model + '_modify'):
            args['frm'] = frm
            return _router.call_ep('$theme@content_' + model + '_modify', args, inp)

        else:
            return _tpl.render('pytsite.content@page/modify', {'frm': frm})

    except _odm.error.EntityNotFound:
        raise _http.error.NotFound()


def propose(args: dict, inp: dict) -> str:
    """Propose content endpoint.
    """
    model = args.get('model')

    frm = _odm_ui.get_m_form(model, redirect=_router.base_url())
    frm.title = None

    _metatag.t_set('title', _lang.t('pytsite.content@propose_content'))

    return _router.call_ep('$theme@content_' + model + '_propose', {
        'form': frm
    })
