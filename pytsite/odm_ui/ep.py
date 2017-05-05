"""ODM UI Endpoints.
"""
from pytsite import tpl as _tpl, http as _http, odm as _odm, admin as _admin, assetman as _assetman, router as _router
from . import _api, _browser

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def browse(model: str) -> str:
    """Render browser.
    """
    _assetman.preload('pytsite.odm_ui@js/odm-ui-browser.js')

    return _admin.render(_tpl.render('pytsite.odm_ui@browser', {
        'table': _browser.Browser(model).render()
    }))


def m_form(model: str, eid: str) -> str:
    """Get entity create/modify form.
    """
    try:
        frm = _api.get_m_form(model, eid if eid != '0' else None)
        return _admin.render_form(frm)

    except _odm.error.EntityNotFound:
        raise _http.error.NotFound()


def d_form(model: str) -> str:
    """Get entity(ies) deletion form.
    """
    # Entities IDs to delete
    ids = _router.request().inp.get('ids', [])
    if isinstance(ids, str):
        ids = [ids]

    # No required arguments has been received
    if not model or not ids:
        raise _http.error.NotFound()

    return _admin.render_form(_api.get_d_form(model, ids))
