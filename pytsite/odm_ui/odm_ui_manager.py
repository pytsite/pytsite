"""ODM UI Manager.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core import router, metatag
from pytsite.core.http.errors import ForbiddenError
from pytsite.core.lang import t
from pytsite.core.odm import odm_manager
from pytsite.core.forms import BaseForm
from pytsite.core.html import Ol, Li, Div
from pytsite.core.widgets.input import HiddenInputWidget
from pytsite.core.widgets.buttons import SubmitButtonWidget, LinkButtonWidget
from pytsite.core.widgets.wrapper import WrapperWidget
from pytsite.core.widgets.static import StaticControlWidget
from pytsite.auth import auth_manager
from .models import ODMUIMixin


def get_m_form(model: str, eid: str=None) -> BaseForm:
    """Get entity modification form.
    """
    eid = eid if eid != '0' else None

    if not eid and not _check_permissions('create', model):
        raise ForbiddenError()
    elif eid and not _check_permissions('modify', model, [eid]):
        raise ForbiddenError()

    form = BaseForm('odm-ui-form')

    # Action, redirect and validation endpoints
    form.validation_ep = 'pytsite.odm_ui.eps.validate_m_form'
    form.action = router.endpoint_url('pytsite.odm_ui.eps.post_m_form', {'model': model, 'id': eid if eid else '0'})
    form.redirect = router.endpoint_url('pytsite.odm_ui.eps.browse', {'model': model})

    # Action buttons
    submit_button = SubmitButtonWidget(uid='action_submit', value=t('pytsite.odm_ui@save'), color='primary', icon='fa fa-save')
    cancel_button_url = router.endpoint_url('pytsite.odm_ui.eps.browse', {'model': model})
    cancel_button = LinkButtonWidget(uid='action_cancel', value=t('pytsite.odm_ui@cancel'), href=cancel_button_url, icon='fa fa-ban')
    actions_wrapper = WrapperWidget(uid='actions')
    actions_wrapper.add_child(submit_button, 10).add_child(cancel_button, 20)
    form.add_widget(actions_wrapper, area='footer')

    # Metadata
    form.add_widget(HiddenInputWidget(name='__model', value=model), area='form')
    form.add_widget(HiddenInputWidget(name='__entity_id', value=eid), area='form')

    # Setting up the form with entity hook
    entity = dispense_entity(model, eid)
    entity.setup_m_form(form)

    if entity.is_new:
        legend = entity.t('odm_ui_' + model + '_create_form_legend')
    else:
        legend = entity.t('odm_ui_' + model + '_modify_form_legend')

    metatag.t_set('title', legend)

    return form


def get_d_form(model: str, ids: list) -> BaseForm:
    """Get entities delete form.
    """
    if not _check_permissions('delete', model, ids):
        raise ForbiddenError()

    form = BaseForm('odm-ui-delete-form')
    form.action = router.endpoint_url('pytsite.odm_ui.eps.post_d_form', {'model': model})
    ol = Ol()

    mock = dispense_entity(model)
    metatag.t_set('title', mock.t('odm_ui_' + model + '_delete_form_legend'))

    for eid in ids:
        entity = dispense_entity(model, eid)
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


def dispense_entity(model: str, entity_id: str=None):
    """Dispense entity.

    :rtype: ODMUIMixin|ODMModel
    """

    if not entity_id or entity_id == '0':
        entity_id = None
    entity = odm_manager.dispense(model, entity_id)
    if not isinstance(entity, ODMUIMixin):
        raise TypeError("Model '{}' doesn't extend 'ODMUIMixin'".format(model))

    return entity


def _check_permissions(perm_type: str, model: str, ids=None) -> bool:
    user = auth_manager.get_current_user()

    if user.is_anonymous():
        return False

    if perm_type == 'create' and user.has_permission('pytsite.odm_ui.create.' + model):
        return True
    elif perm_type == 'modify' or perm_type == 'delete':
        if user.has_permission('pytsite.odm_ui.' + perm_type + '.' + model):
            return True
        elif user.has_permission('pytsite.odm_ui.' + perm_type + '_own.' + model):
            for eid in ids:
                entity = dispense_entity(model, eid)
                if not entity:
                    return False
                if entity.has_field('author') and not entity.f_get('author').id == user.id:
                    return False
            return True

    return False
