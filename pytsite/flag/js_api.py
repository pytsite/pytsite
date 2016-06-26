"""Flag Package Endpoints.
"""
from pytsite import auth as _auth, odm as _odm
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def like(inp: dict) -> dict:
    current_user = _auth.current_user()
    entity = _odm.get_by_ref(inp.get('entity'))

    if current_user.is_anonymous or not entity:
        raise ValueError('Invalid input arguments.')

    return {'status': _api.toggle(entity, current_user), 'count': _api.count(entity)}
