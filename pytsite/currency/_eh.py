"""Event Handlers
"""
from pytsite import form as _form, auth as _auth, auth_ui as _auth_ui, odm as _odm, lang as _lang, widget as _widget
from . import _widget as _currency_widget, _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def odm_ui_user_m_form_setup_widgets(frm: _form.Form, entity: _auth_ui.model.UserUI):
    cnt_wrapper = frm.get_widget('content-wrapper')  # type: _widget.Container
    cnt_wrapper.add_widget(_currency_widget.Select(
        uid='currency',
        weight=105,
        label=_lang.t('pytsite.currency@currency'),
        value=entity.f_get('currency'),
        h_size='col-xs-12 col-sm-6 col-md-5 col-lg-4',
        required=True,
    ))


def odm_model_user_setup(entity: _auth.model.User):
    entity.define_field(_odm.field.String('currency', default=_api.get_main()))


def _get_profile_form_user(frm: _form.Form) -> _auth.model.User:
    if frm.get_widget('__odm_ui_model').value != 'user':
        raise ValueError('Invalid model.')

    user = _auth.get_user(uid=frm.get_widget('__odm_ui_entity_id').value)
    if not user:
        raise ValueError('User is not found.')

    return user
