"""ODM UI Endpoints.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core import tpl as _tpl, lang as _lang, http as _http, router as _router, odm as _odm
from . import _manager, _browser


def browse(args: dict, inp: dict) -> str:
    return _tpl.render('pytsite.odm_ui@admin_browser',
                       {'browser': _browser.ODMUIBrowser(args.get('model')).get_table_skeleton()})


def get_browser_rows(args: dict, inp: dict) -> _http.response.JSONResponse:
    """Get browser rows via AJAX request.
    """
    offset = int(inp.get('offset', 0))
    limit = int(inp.get('limit', 0))
    sort_field = inp.get('sort', None)
    sort_order = inp.get('order', None)

    return _http.response.JSONResponse(
        _browser.ODMUIBrowser(args.get('model')).get_rows(offset, limit, sort_field, sort_order))


def get_m_form(args: dict, inp: dict) -> str:
    """Get entity create/modify form.
    """
    eid = args.get('id') if args.get('id') != '0' else None
    form = _manager.get_m_form(args.get('model'), eid)
    return _tpl.render('pytsite.odm_ui@admin_modify_form', {'form': form})


def validate_m_form(args: dict, inp: dict) -> dict:
    """Validate entity create/modify form.
    """
    global_messages = []
    form = _manager.get_m_form(inp.get('__model'), inp.get('__entity_id'))
    v_status = form.fill(inp, validation_mode=True).validate()
    widget_messages = form.messages

    return {'status': v_status, 'messages': {'global': global_messages, 'widgets': widget_messages}}


def post_m_form(args: dict, inp: dict) -> _http.response.RedirectResponse:
    """Process submit of modify form.
    """

    model = args.get('model')
    entity_id = args.get('id')

    form = _manager.get_m_form(model, entity_id)

    if not form.fill(inp).validate():
        _router.session.add_error(str(form.messages))
        raise _http.error.InternalServerError()

    entity = _manager.dispense_entity(model, entity_id)
    for f_name, f_value in form.values.items():
        if entity.has_field(f_name):
            entity.f_set(f_name, f_value)

    entity.save()

    entity.submit_m_form(form)

    return _http.response.RedirectResponse(form.redirect)


def get_d_form(args: dict, inp: dict) -> str:
    model = args.get('model')

    ids = inp.get('ids', [])
    if isinstance(ids, str):
        ids = [ids]

    if not ids:
        return _http.response.RedirectResponse(_router.endpoint_url('pytsite.odm_ui.eps.browse', {'model': model}))

    form = _manager.get_d_form(model, ids)

    return _tpl.render('pytsite.odm_ui@admin_delete_form', {'form': form})


def post_d_form(args: dict, inp: dict) -> _http.response.RedirectResponse:
    """Submit delete form.
    """

    model = args.get('model')
    ids = inp.get('ids', [])
    if isinstance(ids, str):
        ids = [ids]

    try:
        for eid in ids:
            _manager.dispense_entity(model, eid).delete()
        _router.session.add_info(_lang.t('pytsite.odm_ui@operation_successful'))
    except _odm.error.ForbidEntityDelete as e:
        _router.session.add_error(_lang.t('pytsite.odm_ui@entity_deletion_forbidden') + ': ' + str(e))

    return _http.response.RedirectResponse(_router.endpoint_url('pytsite.odm_ui.eps.browse', {'model': model}))
