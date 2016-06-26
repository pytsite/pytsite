"""PytSite Content HTTP API.
"""
from pytsite import http as _http, auth as _auth, lang as _lang, validation as _validation, odm as _odm
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def patch_view_count(inp: dict) -> int:
    model = inp.get('model')
    eid = inp.get('id')

    if not model:
        raise RuntimeError('Model is not specified.')

    if not eid:
        raise RuntimeError('ID is not specified.')

    if model and eid:
        entity = _api.dispense(model, eid)
        if entity:
            entity.f_inc('views_count').save(False)
            return entity.views_count

    return 0


def get_entity(inp: dict) -> dict:
    user = None
    try:
        user = _auth.current_user()
    except _auth.error.AuthenticationError as e:
        raise _http.error.Forbidden(e)

    # Required arguments
    model = inp.get('model')
    eid = inp.get('id')
    if not model or not eid:
        raise _http.error.InternalServerError('Model or ID is not specified.')

    entity = _api.find(model).where('_id', '=', eid).first()

    return entity.as_dict([f.strip() for f in inp.get('fields', '').split(',')])


def delete_entity(inp: dict):
    model = inp.get('model')
    ids = inp.get('ids')

    if not model:
        raise RuntimeError('Model is not specified.')

    if not ids:
        raise RuntimeError('IDs are not specified.')

    if isinstance(ids, str):
        ids = (ids,)

    count = 0
    for eid in ids:
        _api.dispense(model, eid).delete()
        count += 1

    return count


def post_subscribe(inp: dict) -> dict:
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

    return {'message': _lang.t('pytsite.content@digest_subscription_success')}
