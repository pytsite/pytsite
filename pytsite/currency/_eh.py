"""PytSite Currency Event Handlers.
"""
from pytsite import form as _form, odm as _odm, lang as _lang, widget as _widget, auth as _auth, \
    auth_storage_odm as _auth_storage_odm
from . import _widget as _currency_widget, _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def odm_model_user_setup(entity: _auth_storage_odm.model.ODMUser):
    entity.define_field(_odm.field.String('currency', default=_api.get_main()))


def odm_ui_user_m_form_setup_widgets(frm: _form.Form, entity: _auth_storage_odm.model.ODMUser):
    cnt_wrapper = frm.get_widget('content-wrapper')  # type: _widget.Container
    cnt_wrapper.add_widget(_currency_widget.Select(
        uid='currency',
        weight=105,
        label=_lang.t('pytsite.currency@currency'),
        value=entity.f_get('currency'),
        h_size='col-xs-12 col-sm-6 col-md-5 col-lg-4',
        required=True,
    ))


def auth_http_api_get_user(user: _auth.model.AbstractUser, response: dict):
    if not isinstance(user, _auth_storage_odm.model.User):
        return

    c_user = _auth.get_current_user()
    if c_user == user or c_user.is_admin:
        response['currency'] = user.get_field('currency')
