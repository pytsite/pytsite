"""ODM UI Endpoints.
"""
from pytsite import tpl as _tpl, http as _http, odm as _odm, admin as _admin
from . import _api, _browser

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def browse(args: dict, inp: dict) -> str:
    """Render browser.
    """
    return _admin.render(_tpl.render('pytsite.odm_ui@browser', {
        'table': _browser.Browser(args.get('model')).render()
    }))


def m_form(args: dict, inp: dict) -> str:
    """Get entity create/modify form.
    """
    try:
        frm = _api.get_m_form(args.get('model'), args['id'] if args.get('id') != 0 else None)
        return _admin.render_form(frm)

    except _odm.error.EntityNotFound:
        raise _http.error.NotFound()


def d_form(args: dict, inp: dict) -> str:
    """Get entity(ies) deletion form.
    """
    model = args.get('model')

    # Entities IDs to delete
    ids = inp.get('ids', [])
    if isinstance(ids, str):
        ids = [ids]

    # No required arguments has been received
    if not model or not ids:
        return _http.error.NotFound()

    return _admin.render_form(_api.get_d_form(model, ids))
