"""ODM UI Endpoints.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core import tpl
from pytsite.core.form import BaseForm
from pytsite.core.http.response import RedirectResponse, JSONResponse
from pytsite.core.odm import odm_manager
from pytsite.core.lang import t
from pytsite.core import router
from pytsite.core.widgets.input import HiddenInputWidget
from pytsite.core.widgets.wrapper import WrapperWidget
from pytsite.core.widgets.button import SubmitButtonWidget, LinkButtonWidget
from .browser import ODMUIBrowser
from .models import ODMUIMixin


def browse(args: dict, inp: dict) -> str:
    return tpl.render('pytsite.odm_ui@admin_browser', {'browser': ODMUIBrowser(args.get('model'))})


def get_m_form(args: dict, inp: dict) -> str:
    """Get entity create/modify form.
    """

    form = _create_m_form(args.get('model'), args.get('id'))

    return tpl.render('pytsite.odm_ui@admin_modify_form', {'form': form})


def validate_m_form(args: dict, inp: dict) -> dict:
    """Validate entity create/modify form.
    """

    form = _create_m_form(inp.get('__model'), inp.get('__entity_id'))
    v_status = form.fill(inp).validate()

    return {'status': v_status, 'messages': form.messages}


def post_m_form(args: dict, inp: dict) -> RedirectResponse:
    """Process submit of modify form.
    """

    model = args.get('model')
    entity_id = args.get('id')

    form = _create_m_form(model, entity_id)

    if not form.fill(inp).validate():
        pass

    entity = _dispense_entity(model, entity_id)


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

    return form


def _dispense_entity(model: str, entity_id: str) -> ODMUIMixin:
    if entity_id == '0':
        entity_id = None
    entity = odm_manager.dispense(model, entity_id)
    if not isinstance(entity, ODMUIMixin):
        raise TypeError("Model '{}' doesn't extend 'ODMUIMixin'".format(model))

    return entity
