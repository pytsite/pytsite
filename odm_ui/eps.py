"""ODM UI Endpoints.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core import tpl, metatag
from pytsite.core.forms import BaseForm
from pytsite.core.http.errors import ServerError
from pytsite.core.http.response import RedirectResponse, JSONResponse
from pytsite.core.odm import odm_manager
from pytsite.core.odm.models import ODMModel
from pytsite.core.lang import t
from pytsite.core import router
from pytsite.core.html import Ol, Li, Div
from pytsite.core.widgets.input import HiddenInputWidget
from pytsite.core.widgets.wrapper import WrapperWidget
from pytsite.core.widgets.static import StaticControlWidget
from pytsite.core.widgets.buttons import SubmitButtonWidget, LinkButtonWidget
from .browser import ODMUIBrowser
from .models import ODMUIMixin


def browse(args: dict, inp: dict) -> str:
    return tpl.render('pytsite.odm_ui@admin_browser', {'browser': ODMUIBrowser(args.get('model')).get_table_skeleton()})


def get_browser_rows(args: dict, inp: dict) -> JSONResponse:
    """Get browser rows via AJAX request.
    """

    offset = int(inp.get('offset', 0))
    limit = int(inp.get('limit', 0))
    sort_field = inp.get('sort', None)
    sort_order = inp.get('order', None)
    return JSONResponse(ODMUIBrowser(args.get('model')).get_rows(offset, limit, sort_field, sort_order))


def get_m_form(args: dict, inp: dict) -> str:
    """Get entity create/modify form.
    """

    form = _create_m_form(args.get('model'), args.get('id'))

    return tpl.render('pytsite.odm_ui@admin_modify_form', {'form': form})


def validate_m_form(args: dict, inp: dict) -> dict:
    """Validate entity create/modify form.
    """

    global_messages = []

    form = _create_m_form(inp.get('__model'), inp.get('__entity_id'))
    v_status = form.fill(inp, validation_mode=True).validate()
    widget_messages = form.messages

    return {'status': v_status, 'messages': {'global': global_messages, 'widgets': widget_messages}}


def post_m_form(args: dict, inp: dict) -> RedirectResponse:
    """Process submit of modify form.
    """

    model = args.get('model')
    entity_id = args.get('id')

    form = _create_m_form(model, entity_id)

    if not form.fill(inp).validate():
        router.session.add_error(str(form.messages))
        raise ServerError()

    entity = _dispense_entity(model, entity_id)
    for f_name, f_value in form.values.items():
        if entity.has_field(f_name):
            entity.f_set(f_name, f_value)

    entity.save()

    return RedirectResponse(router.endpoint_url('pytsite.odm_ui.eps.browse', {'model': model}))


def get_d_form(args: dict, inp: dict) -> str:
    model = args.get('model')

    ids = inp.get('ids', [])
    if isinstance(ids, str):
        ids = [ids]

    if not ids:
        return RedirectResponse(router.endpoint_url('pytsite.odm_ui.eps.browse', {'model': model}))

    form = _create_d_form(model, ids)

    return tpl.render('pytsite.odm_ui@admin_delete_form', {'form': form})


def post_d_form(args: dict, inp: dict) -> RedirectResponse:
    """Submit delete form.
    """

    model = args.get('model')
    ids = inp.get('ids', [])
    if isinstance(ids, str):
        ids = [ids]

    try:
        for eid in ids:
            _dispense_entity(model, eid).delete()
        router.session.add_info(t('pytsite.odm_ui@operation_successful'))
    except Exception as e:
        router.session.add_error(str(e))

    return RedirectResponse(router.endpoint_url('pytsite.odm_ui.eps.browse', {'model': model}))


def _create_m_form(model: str, entity_id: str) -> BaseForm:
    form = BaseForm('odm-ui-form')

    # Action and validation endpoints
    form.validation_ep = 'pytsite.odm_ui.eps.validate_m_form'
    form.action = router.endpoint_url('pytsite.odm_ui.eps.post_m_form', {'model': model, 'id': entity_id})

    # Action buttons
    submit_button = SubmitButtonWidget(value=t('pytsite.odm_ui@save'), color='primary', icon='fa fa-save')
    cancel_button_url = router.endpoint_url('pytsite.odm_ui.eps.browse', {'model': model})
    cancel_button = LinkButtonWidget(value=t('pytsite.odm_ui@cancel'), href=cancel_button_url, icon='fa fa-ban')
    actions_wrapper = WrapperWidget()
    actions_wrapper.add_child(submit_button, 10).add_child(cancel_button, 20)
    form.add_widget(actions_wrapper, area='footer')

    # Metadata
    form.add_widget(HiddenInputWidget(name='__model', value=model), area='form')
    form.add_widget(HiddenInputWidget(name='__entity_id', value=entity_id), area='form')

    # Setting up the form with entity hook
    entity = _dispense_entity(model, entity_id)
    entity.setup_m_form(form)

    if entity.is_new:
        legend = entity.t('odm_ui_' + model + '_create_form_legend')
    else:
        legend = entity.t('odm_ui_' + model + '_modify_form_legend')

    metatag.set_tag('title', legend)

    return form


def _create_d_form(model: str, entity_ids: list) -> BaseForm:
    """Create delete form.
    """

    form = BaseForm('odm-ui-delete-form')
    form.action = router.endpoint_url('pytsite.odm_ui.eps.post_d_form', {'model': model})
    ol = Ol()

    mock = _dispense_entity(model)
    metatag.set_tag('title', mock.t(model + '_delete_form_legend'))

    for eid in entity_ids:
        entity = _dispense_entity(model, eid)
        form.add_widget(HiddenInputWidget(name='ids', value=str(entity.id)))
        ol.append(Li(entity.get_d_form_description()))

    form.add_widget(StaticControlWidget(html_em=Div, value=str(ol)))

    # Action buttons
    submit_button = SubmitButtonWidget(value=t('pytsite.odm_ui@delete'), color='danger', icon='fa fa-save')
    cancel_button_url = router.endpoint_url('pytsite.odm_ui.eps.browse', {'model': model})
    cancel_button = LinkButtonWidget(value=t('pytsite.odm_ui@cancel'), href=cancel_button_url, icon='fa fa-ban')
    actions_wrapper = WrapperWidget()
    actions_wrapper.add_child(submit_button, 10).add_child(cancel_button, 20)
    form.add_widget(actions_wrapper, area='footer')

    return form


def _dispense_entity(model: str, entity_id: str=None):
    """Dispense entity.

    :rtype: ODMUIMixin|ODMModel
    """

    if not entity_id or entity_id == '0':
        entity_id = None
    entity = odm_manager.dispense(model, entity_id)
    if not isinstance(entity, ODMUIMixin):
        raise TypeError("Model '{}' doesn't extend 'ODMUIMixin'".format(model))

    return entity
