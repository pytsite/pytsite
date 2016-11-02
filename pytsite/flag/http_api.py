"""Flag Package Endpoints.
"""
from pytsite import auth as _auth, odm as _odm, http as _http
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def patch_toggle(**kwargs) -> dict:
    """Set/remove flag.
    """
    # Check for permissions
    if _auth.get_current_user().is_anonymous:
        raise _http.error.Unauthorized('Anonymous users are not allowed here.')

    # Check for entity model
    model = kwargs.get('model')
    if not model:
        raise RuntimeError('Model is not specified.')

    # Check for entity ID
    uid = kwargs.get('uid')
    if not uid:
        raise RuntimeError('Entity UID is not specified.')

    try:
        entity = _odm.dispense(model, uid)
        count = _api.toggle(entity)
        is_flagged = _api.is_flagged(entity)

        return {
            'count': count,
            'status': is_flagged,
        }

    except _odm.error.ForbidEntityOperation as e:
        raise _http.error.Forbidden(str(e))
