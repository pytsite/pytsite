"""Content Plugin Endpoints.
"""
import re as _re
from datetime import datetime as _datetime
from pytsite import taxonomy as _taxonomy, odm_ui as _odm_ui, auth as _auth, reg as _reg, http as _http, \
    router as _router, metatag as _metatag, assetman as _assetman, odm as _odm, widget as _widget, \
    lang as _lang, validation as _validation, logger as _logger, hreflang as _hreflang, comments as _comments

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def index(args: dict, inp: dict):
    """Content Index.
    """
    # Delayed import to prevent exception during application initialization
    from . import _api

    # Checking if the model is registered
    model = args.get('model')
    if not model or not _api.is_model_registered(model):
        _logger.warn("Content model '{}' is not found. Redirecting to home.".format(model), __name__)
        return _http.response.Redirect(_router.base_url())

    # Getting finder
    f = _api.find(model)

    # Filter by term
    term_field = args.get('term_field')
    if term_field:
        term_model = f.mock.get_field(term_field).model
        term_alias = args.get('term_alias')
        if term_alias:
            term = _taxonomy.find(term_model).where('alias', '=', term_alias).first()
            if term:
                args['term'] = term
                if isinstance(f.mock.fields[term_field], _odm.field.Ref):
                    f.where(term_field, '=', term)
                elif isinstance(f.mock.fields[term_field], _odm.field.RefsList):
                    f.where(term_field, 'in', [term])
                _metatag.t_set('title', term.title)
            else:
                raise _http.error.NotFound()
        else:
            raise _http.error.NotFound()

    # Filter by author
    author_identifier = inp.get('author') or args.get('author')
    if author_identifier:
        if _re.match('^[a-f0-9]{24}$', author_identifier):
            author = _auth.get_user(uid=author_identifier)
        else:
            author = _auth.get_user(nickname=author_identifier)

        if author:
            _metatag.t_set('title', _lang.t('pytsite.content@articles_of_author', {'name': author.full_name}))
            f.where('author', '=', author)
            args['author'] = author
        else:
            raise _http.error.NotFound()

    # Search
    if inp.get('search'):
        query = inp.get('search')
        f.where_text(query)
        _metatag.t_set('title', _lang.t('pytsite.content@search', {'query': query}))

    pager = _widget.static.Pager('content-pager', total_items=f.count(), per_page=10)

    args['entities'] = list(f.skip(pager.skip).get(pager.limit))
    args['pager'] = pager
    endpoint = _reg.get('content.endpoints.view.' + model, '$theme.ep.' + model + '_index')

    return _router.call_ep(endpoint, args, inp)


def view(args: dict, inp: dict):
    """View Content Entity.
    """
    from . import _api

    model = args.get('model')
    entity = _api.find(model, None, False).where('_id', '=', args.get('id')).first()
    """:type: pytsite.content._model.Content"""

    if not entity:
        raise _http.error.NotFound()

    # Checking publish time
    if entity.publish_time > _datetime.now():
        if not _auth.get_current_user().has_permission('pytsite.odm_ui.modify.' + entity.model):
            raise _http.error.Forbidden()

    # Update comments count
    entity.f_set('comments_count', _comments.get_all_comments_count(entity.url)).save(True, False)

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
        image_url = entity.images[0].f_get('url', width=image_w, height=image_h)
        _metatag.t_set('og:image', image_url)
        _metatag.t_set('og:image:width', str(image_w))
        _metatag.t_set('og:image:height', str(image_h))
        _metatag.t_set('twitter:image', image_url)
    else:
        _metatag.t_set('twitter:card', 'summary')

    # Other metatags
    _metatag.t_set('og:type', 'article')
    _metatag.t_set('author', entity.author.full_name)
    _metatag.t_set('article:author', entity.author.full_name)
    _metatag.t_set('og:url', entity.url)
    _metatag.t_set('article:publisher', entity.url)

    # Alternate languages URLs
    for lng in _lang.langs(False):
        f_name = 'localization_' + lng
        if entity.has_field(f_name) and entity.f_get(f_name):
            _hreflang.add(lng, entity.f_get(f_name).url)

    _assetman.add('pytsite.content@js/content.js')

    args['entity'] = entity
    endpoint = _reg.get('content.endpoints.view.' + model, '$theme.ep.' + model + '_view')

    return _router.call_ep(endpoint, args, inp)


def view_count(args: dict, inp: dict) -> int:
    model = inp.get('model')
    eid = inp.get('id')

    if model and eid:
        from . import _api
        entity = _api.find(model).where('_id', '=', eid).first()
        if entity:
            entity.f_inc('views_count').save(skip_hooks=True, update_timestamp=False)
            return entity.f_get('views_count')

    return 0


def propose(args: dict, inp: dict) -> str:
    """Propose content endpoint.
    """
    model = args.get('model')
    endpoint = _reg.get('content.endpoints.propose.' + model, '$theme.ep.' + model + '_propose')

    frm = _odm_ui.get_m_form(model, redirect=_router.base_url())
    frm.title = None
    frm.get_widget('action-cancel').href = _router.base_url()

    _metatag.t_set('title', _lang.t('pytsite.content@propose_content'))

    return _router.call_ep(endpoint, {
        'form': frm
    })


def subscribe(args: dict, inp: dict) -> str:
    """Subscribe to digest endpoint.
    """
    email = inp.get('email')
    _validation.rule.Email(value=email).validate()

    lng = _lang.get_current()

    s = _odm.find('content_subscriber').where('email', '=', email).where('language', '=', lng).first()
    if s:
        if not s.f_get('enabled'):
            s.f_set('enabled', True)
    else:
        s = _odm.dispense('content_subscriber').f_set('email', email).f_set('language', lng)

    s.save()

    return _lang.t('pytsite.content@digest_subscription_success')


def unsubscribe(args: dict, inp: dict) -> _http.response.Redirect:
    """Unsubscribe from digest endpoint.
    """
    s = _odm.dispense('content_subscriber', args.get('id'))
    if s:
        s.f_set('enabled', False).save()
        _router.session().add_success(_lang.t('pytsite.content@unsubscription_successful'))

    return _http.response.Redirect(_router.base_url())


def ajax_search(args: dict, inp: dict) -> _http.response.JSON:
    from . import _api

    # Query is mandatory parameter
    query = inp.get('q')
    if not query:
        return _http.response.JSON({'results': ()})

    # Anonymous users cannot perform search
    user = _auth.get_current_user()
    if user.is_anonymous:
        raise _http.error.Forbidden()

    model = args.get('model')
    language = inp.get('language', _lang.get_current())

    # User can browse ANY entities
    if user.has_permission('pytsite.odm_ui.browse.' + model):
        f = _api.find(model, status=None, check_publish_time=None, language=language)
    # User can browse only its OWN entities
    elif user.has_permission('pytsite.odm_ui.browse_own.' + model):
        f = _api.find(model, status=None, check_publish_time=None, language=language)
        f.where('author', '=', user)
    # User cannot browse entities, so its rights equals to the anonymous user
    else:
        f = _api.find(model, language=language)

    f.sort([('title', _odm.I_ASC)]).where('title', 'regex_i', query)
    r = [{'id': e.model + ':' + str(e.id), 'text': e.title} for e in f.get(20)]

    return _http.response.JSON({'results': r})
