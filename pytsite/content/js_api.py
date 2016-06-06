"""PytSite Content JS API Endpoints.
"""
from pytsite import lang as _lang, auth as _auth, http as _http, odm as _odm, validation as _validation

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def view_count(inp: dict) -> int:
    model = inp.get('model')
    eid = inp.get('id')

    if model and eid:
        from . import _api
        entity = _api.find(model).where('_id', '=', eid).first()
        if entity:
            entity.f_inc('views_count').save(skip_hooks=True, update_timestamp=False)
            return entity.f_get('views_count')

    return 0


def search(inp: dict) -> dict:
    from . import _api

    # Query is mandatory parameter
    query = inp.get('q')
    if not query:
        return {'results': ()}

    # Anonymous users cannot perform search
    user = _auth.get_current_user()
    if user.is_anonymous:
        raise _http.error.Forbidden()

    model = inp.get('model')
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

    return {'results': r}


def subscribe(inp: dict) -> str:
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
