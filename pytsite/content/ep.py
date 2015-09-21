"""Content Plugin Endpoints.
"""
import re as _re
from datetime import datetime as _datetime
from pytsite import disqus as _disqus, taxonomy as _taxonomy, odm_ui as _odm_ui, auth as _auth, reg as _reg, \
    http as _http, router as _router, metatag as _metatag, assetman as _assetman, odm as _odm, widget as _widget, \
    lang as _lang, validation as _validation, logger as _logger, browser as _browser

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def index(args: dict, inp: dict):
    """Content Index.
    """
    # Delayed import to prevent exception during application initialization
    from . import _functions

    # Checking if the model is registered
    model = args.get('model')
    if not model or not _functions.is_model_registered(model):
        _logger.error("Content model '{}' is not found. Redirecting to home.".format(model), __name__)
        return _http.response.Redirect(_router.base_url())

    # Getting finder
    f = _functions.find(model)

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

    pager = _widget.static.Pager(f.count(), 10)

    args['entities'] = list(f.skip(pager.skip).get(pager.limit))
    args['pager'] = pager
    endpoint = _reg.get('content.endpoints.view.' + model, 'app.ep.' + model + '_index')

    return _router.call_ep(endpoint, args, inp)


def view(args: dict, inp: dict):
    """View Content Entity.
    """
    from . import _functions

    model = args.get('model')
    entity = _functions.find(model, None, False).where('_id', '=', args.get('id')).first()
    """:type: pytsite.content._model.Content"""

    if not entity:
        raise _http.error.NotFound()

    # Checking publish time
    if entity.publish_time > _datetime.now():
        if not _auth.get_current_user().has_permission('pytsite.odm_ui.modify.' + entity.model):
            raise _http.error.Forbidden()

    # Recalculate comments count
    try:
        current_cc = entity.f_get('comments_count')
        actual_cc = _disqus.functions.get_comments_count(_router.current_url(True))
        if actual_cc != current_cc:
            entity.f_set('comments_count', actual_cc).save()
    except ValueError:
        pass

    # Meta title
    title = entity.title
    _metatag.t_set('title', title)
    _metatag.t_set('og:title', title)
    _metatag.t_set('twitter:title', title)

    # Meta description
    description = entity.description
    _metatag.t_set('description', description)
    _metatag.t_set('og:description', description)
    _metatag.t_set('twitter:description', description)

    # Meta keywords
    _metatag.t_set('keywords', entity.f_get('tags', as_string=True))

    # Meta image
    if entity.images:
        _metatag.t_set('twitter:card', 'summary_large_image')
        image_w = 900
        image_h = 470
        image_url = entity.images[0].f_get('url', width=image_w, height=image_h)
        _metatag.t_set('og:image', image_url)
        _metatag.t_set('og:image:width', str(image_w))
        _metatag.t_set('og:image:height', str(image_h))
        _metatag.t_set('twitter:image', image_url)
    else:
        _metatag.t_set('twitter:card', 'summary')

    # Meta author and URL
    _metatag.t_set('author', entity.author.full_name)
    _metatag.t_set('article:author', entity.author.full_name)
    _metatag.t_set('og:url', entity.url)
    _metatag.t_set('article:publisher', entity.url)

    endpoint = _reg.get('content.endpoints.view.' + model, 'app.ep.' + model + '_view')

    _assetman.add('pytsite.content@js/content.js')

    return _router.call_ep(endpoint, {'entity': entity})


def view_count(args: dict, inp: dict) -> int:
    model = inp.get('model')
    eid = inp.get('id')

    if model and eid:
        from . import _functions
        entity = _functions.find(model).where('_id', '=', eid).first()
        if entity:
            entity.f_inc('views_count').save(skip_hooks=True, update_timestamp=False)
            return entity.f_get('views_count')

    return 0


def propose(args: dict, inp: dict) -> str:
    """Propose content endpoint.
    """
    model = args.get('model')
    endpoint = _reg.get('content.endpoints.propose.' + model, 'app.ep.' + model + '_propose')

    form = _odm_ui.get_m_form(model)
    form.get_widget('actions').get_child('action_cancel').href = _router.base_url()
    form.redirect = _router.base_url()

    _metatag.t_set('title', _lang.t('pytsite.content@propose_content'))

    return _router.call_ep(endpoint, {
        'form': form
    })


def subscribe(args: dict, inp: dict) -> str:
    """Subscribe to digest endpoint.
    """
    email = inp.get('email')
    if not _validation.rule.Email(value=email).validate():
        raise Exception(_lang.t('pytsite.content@invalid_email'))

    s = _odm.find('content_subscriber').where('email', '=', email).first()
    if s:
        if not s.f_get('enabled'):
            s.f_set('enabled', True).save()
    else:
        _odm.dispense('content_subscriber').f_set('email', email).save()

    return _lang.t('pytsite.content@digest_subscription_success')


def unsubscribe(args: dict, inp: dict) -> _http.response.Redirect:
    """Unsubscribe from digest endpoint.
    """
    sid = args.get('id')
    s = _odm.dispense('content_subscriber', sid)
    if s:
        s.f_set('enabled', False).save()
        _router.session.add_success(_lang.t('pytsite.content@unsubscription_successful'))

    return _http.response.Redirect(_router.base_url())
