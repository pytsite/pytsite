"""PytSite Content HTTP API.
"""
from pytsite import http as _http, auth as _auth, lang as _lang, validation as _validation, odm as _odm, \
    odm_auth as _odm_auth
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def patch_view_count(inp: dict) -> int:
    """Increase content entity views counter by one.
    """
    model = inp.get('model')
    eid = inp.get('id')

    if not model:
        raise RuntimeError('Model is not specified.')

    if not eid:
        raise RuntimeError('ID is not specified.')

    if model and eid:
        entity = _api.dispense(model, eid)
        if entity:
            with entity:
                _auth.switch_user_to_system()
                entity.f_inc('views_count').save(update_timestamp=False)
                _auth.restore_user()

            return entity.views_count

    return 0


def post_subscribe(inp: dict) -> dict:
    """Subscribe to digest endpoint.
    """
    email = inp.get('email')
    _validation.rule.Email(value=email).validate()

    lng = _lang.get_current()

    s = _odm.find('content_subscriber').eq('email', email).eq('language', lng).first()
    if s:
        if not s.f_get('enabled'):
            with s:
                s.f_set('enabled', True).save()
    else:
        # Create new
        _odm.dispense('content_subscriber').f_set('email', email).f_set('language', lng).save()

    return {'message': _lang.t('pytsite.content@digest_subscription_success')}


def get_widget_entity_select_search(inp: dict) -> dict:
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
    if user.has_permission('pytsite.odm_perm.view.' + model):
        f = _api.find(model, status=None, check_publish_time=None, language=language)

    # User can browse only its OWN entities
    elif user.has_permission('pytsite.odm_perm.view_own.' + model):
        f = _api.find(model, status=None, check_publish_time=None, language=language)
        f.eq('author', user.uid)

    # User cannot browse entities, so its rights equals to the anonymous user
    else:
        f = _api.find(model, language=language)

    f.sort([('title', _odm.I_ASC)]).where('title', 'regex_i', query)
    r = [{'id': e.model + ':' + str(e.id), 'text': e.title} for e in f.get(20)]

    return {'results': r}
