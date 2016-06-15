"""PytSite Content HTTP API.
"""
from pytsite import http as _http, auth as _auth
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


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
