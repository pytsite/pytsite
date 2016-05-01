"""ODM UI Endpoints.
"""
from typing import Union as _Union
from pytsite import tpl as _tpl, lang as _lang, http as _http, odm as _odm, logger as _logger, router as _router, \
    admin as _admin, form as _form
from . import _api, _browser

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def browse(args: dict, inp: dict) -> str:
    """Render browser.
    """
    table = _browser.Browser(args.get('model')).get_table()

    return _admin.render(_tpl.render('pytsite.odm_ui@browser', {'table': table}))


def browse_get_rows(args: dict, inp: dict) -> _http.response.JSON:
    """Get browser rows via AJAX request.
    """
    offset = int(inp.get('offset', 0))
    limit = int(inp.get('limit', 0))
    sort_field = inp.get('sort')
    sort_order = inp.get('order')
    search = inp.get('search')
    browser = _browser.Browser(args.get('model'))
    rows = browser.get_rows(offset, limit, sort_field, sort_order, search)

    return _http.response.JSON(rows)


def m_form(args: dict, inp: dict) -> str:
    """Get entity create/modify form.
    """
    try:
        return _admin.render_form(_api.get_m_form(args.get('model'), args['id'] if args.get('id') != 0 else None))
    except _odm.error.EntityNotFound:
        raise _http.error.NotFound()


def m_form_submit(args: dict, inp: dict) -> _http.response.Redirect:
    """Process submit of modify form.
    """
    model = args.get('model')
    entity_id = args.get('id')

    # Re-constructing the form
    frm = _api.get_m_form(model, entity_id).fill(inp, mode='validation')

    # Validate the form
    try:
        frm.validate()
    except _form.error.ValidationError as e:
        _router.session().add_error(str(e.errors))
        raise _http.error.InternalServerError()

    # Re-fill form in 'normal' mode
    frm.fill(inp)

    # Dispense entity
    entity = _api.dispense_entity(model, entity_id)

    # Let entity know about form submission
    entity.ui_m_form_submit(frm)

    # Populate form values to entity
    for f_name, f_value in frm.values.items():
        if entity.has_field(f_name):
            entity.f_set(f_name, f_value)

    try:
        # Save entity
        entity.save()
        _router.session().add_info(_lang.t('pytsite.odm_ui@operation_successful'))
    except Exception as e:
        _router.session().add_error(str(e))
        _logger.error(str(e), __name__)

    return _http.response.Redirect(frm.redirect)


def d_form(args: dict, inp: dict) -> str:
    """Get entity deletion form.
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


def d_form_submit(args: dict, inp: dict) -> _Union[_http.response.Redirect, _http.response.JSON]:
    """Submit delete form.
    """
    model = args.get('model')
    json = inp.get('json')
    ids = inp.get('ids', ())

    if isinstance(ids, str):
        ids = [ids]

    try:
        # Delete entities
        for eid in ids:
            _api.dispense_entity(model, eid).delete()

        if json:
            return _http.response.JSON({'status': True})
        else:
            _router.session().add_info(_lang.t('pytsite.odm_ui@operation_successful'))

    # Entity deletion was forbidden
    except _odm.error.ForbidEntityDelete as e:
        if json:
            return _http.response.JSON({'status': False, 'error': str(e)}, 403)
        else:
            _router.session().add_error(_lang.t('pytsite.odm_ui@entity_deletion_forbidden') + '. ' + str(e))

    redirect = inp.get('__redirect', _router.ep_url('pytsite.odm_ui.ep.browse', {'model': model}))

    return _http.response.Redirect(redirect)
