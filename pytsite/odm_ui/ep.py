"""ODM UI Endpoints.
"""
from typing import Union as _Union
from pytsite import tpl as _tpl, lang as _lang, http as _http, odm as _odm, logger as _logger, router as _router, \
    admin as _admin, form as _form, errors as _errors
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
        return _admin.render_form(_api.get_m_form(args.get('model'), args['id'] if args.get('id') != 0 else None))

    except _odm.error.EntityNotFound:
        raise _http.error.NotFound()


def m_form_submit(args: dict, inp: dict) -> _http.response.Redirect:
    """Process submit of modify form.
    """
    model = args.get('model')
    entity_id = args.get('id')

    # Create the form
    frm = _api.get_m_form(model, entity_id)

    # Switch form to tha last step, as some widgets can be added dynamically
    frm.step = frm.steps

    # Fill the form in 'validation' mode
    frm.fill(inp, mode='validation')

    # Validate the form
    try:
        frm.validate()
    except _form.error.ValidationError as e:
        _router.session().add_error_message(str(e.errors))
        raise _http.error.InternalServerError()

    # Refill the form in 'normal' mode
    frm.fill(inp)

    # Dispense entity
    entity = _api.dispense_entity(model, entity_id)

    entity.lock()

    # Let entity know about form submission
    entity.odm_ui_m_form_submit(frm)

    # Populate form values to entity
    for f_name, f_value in frm.values.items():
        if entity.has_field(f_name):
            entity.f_set(f_name, f_value)

    try:
        # Save entity
        entity.save()
        _router.session().add_info_message(_lang.t('pytsite.odm_ui@operation_successful'))

    except Exception as e:
        _router.session().add_error_message(str(e))
        _logger.error(str(e), exc_info=e, stack_info=True)
        raise e

    finally:
        entity.unlock()

    frm.submit()

    # Process 'special' redirect endpoint
    if frm.redirect == 'ENTITY_VIEW':
        frm.redirect = entity.odm_ui_view_url()

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
    ids = inp.get('ids', ())

    if isinstance(ids, str):
        ids = [ids]

    try:
        # Delete entities
        for eid in ids:
            entity = _api.dispense_entity(model, eid).odm_ui_d_form_submit()

        _router.session().add_info_message(_lang.t('pytsite.odm_ui@operation_successful'))

    # Entity deletion was forbidden
    except _errors.ForbidDeletion as e:
        _logger.error(str(e), exc_info=e)
        _router.session().add_error_message(_lang.t('pytsite.odm_ui@entity_deletion_forbidden') + '. ' + str(e))

    default_redirect = _router.ep_url('pytsite.odm_ui@browse', {'model': model})
    return _http.response.Redirect(inp.get('__redirect', default_redirect))
