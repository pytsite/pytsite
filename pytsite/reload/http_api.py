"""PytSite Reload HTTP API.
"""
from pytsite import auth as _auth, http as _http
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def post_reload(**kwargs) -> dict:
    if not _auth.get_current_user().has_permission('pytsite.reload.reload'):
        raise _http.error.Forbidden('Insufficient permissions.')

    _api.reload(False)

    return {'status': True}
