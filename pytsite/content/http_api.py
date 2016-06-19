"""PytSite Content HTTP API.
"""
from pytsite import http as _http, auth as _auth
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
            entity.f_inc('views_count').save(skip_hooks=True, update_timestamp=False)
            return entity.views_count

    return 0


def get_entity(inp: dict) -> dict:
    user = None
    try:
        user = _auth.get_current_user()
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
