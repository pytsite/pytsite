"""ODM UI Endpoints.
"""
from pytsite import tpl as _tpl, lang as _lang, http as _http, odm as _odm, logger as _logger, router as _router
from . import _functions, _browser

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def browse(args: dict, inp: dict) -> str:
    """Render browser.
    """
    browser = _browser.Browser(args.get('model'))
    table = browser.get_table_skeleton()
    return _tpl.render('pytsite.odm_ui@admin_browser', {'table': table})


def get_browser_rows(args: dict, inp: dict) -> _http.response.JSON:
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


def get_m_form(args: dict, inp: dict) -> str:
    """Get entity create/modify form.
    """
    eid = args.get('id') if args.get('id') != '0' else None
    try:
        form = _functions.get_m_form(args.get('model'), eid)
        return _tpl.render('pytsite.odm_ui@admin_modify_form', {'form': form})
    except _odm.error.EntityNotFound:
        raise _http.error.NotFound()


def validate_m_form(args: dict, inp: dict) -> dict:
    """Validate entity create/modify form.
    """
    global_messages = []

    model = inp.get('__model')
    entity_id = inp.get('__entity_id')
    if not model:
        return {'status': True}

    form = _functions.get_m_form(model, entity_id, 'validate')
    v_status = form.fill(inp, validation_mode=True).validate()
    widget_messages = form.messages

    return {'status': v_status, 'messages': {'global': global_messages, 'widgets': widget_messages}}


def post_m_form(args: dict, inp: dict) -> _http.response.Redirect:
    """Process submit of modify form.
    """
    model = args.get('model')
    entity_id = args.get('id')

    # Create form
    form = _functions.get_m_form(model, entity_id, 'submit')

    # Fill and validate form
    if not form.fill(inp).validate():
        _router.session.add_error(str(form.messages))
        raise _http.error.InternalServerError()

    # Dispense entity and populate its fields with form's values
    entity = _functions.dispense_entity(model, entity_id)
    for f_name, f_value in form.values.items():
        if entity.has_field(f_name):
            entity.f_set(f_name, f_value)

    try:
        entity.submit_m_form(form)  # Entity hook
        entity.save()
        _router.session.add_info(_lang.t('pytsite.odm_ui@operation_successful'))
    except Exception as e:
        _router.session.add_error(str(e))
        _logger.error(str(e), __name__)

    return _http.response.Redirect(form.redirect)


def get_d_form(args: dict, inp: dict) -> str:
    model = args.get('model')

    # Entities IDs to delete
    ids = inp.get('ids', [])
    if isinstance(ids, str):
        ids = [ids]

    # No required arguments has been received
    if not model or not ids:
        return _http.error.NotFound()

    form = _functions.get_d_form(model, ids, _router.ep_url('pytsite.odm_ui.ep.browse', {'model': model}))

    return _tpl.render('pytsite.odm_ui@admin_delete_form', {'form': form})


def post_d_form(args: dict, inp: dict) -> _http.response.Redirect:
    """Submit delete form.

    :rtype _http.response.Redirect | _http.response.JSON
    """
    model = args.get('model')
    json = inp.get('json')
    ids = inp.get('ids', ())

    if isinstance(ids, str):
        ids = [ids]

    try:
        if not _functions.check_permissions('delete', model, ids):
            if json:
                return _http.response.JSON({'status': False, 'error': 'Forbidden'}, 403)
            else:
                raise _http.error.Forbidden()

        for eid in ids:
            _functions.dispense_entity(model, eid).delete()

        if json:
            return _http.response.JSON({'status': True})
        else:
            _router.session.add_info(_lang.t('pytsite.odm_ui@operation_successful'))
    except _odm.error.ForbidEntityDelete as e:
        if json:
            return _http.response.JSON({'status': False, 'error': str(e)}, 403)
        else:
            _router.session.add_error(_lang.t('pytsite.odm_ui@entity_deletion_forbidden') + '. ' + str(e))

    redirect = inp.get('__form_redirect', _router.ep_url('pytsite.odm_ui.ep.browse', {'model': model}))

    return _http.response.Redirect(redirect)
