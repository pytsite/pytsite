"""Event Handlers
"""
from pytsite import form as _form, auth as _auth
from . import _widget

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def auth_profile_form_render(frm: _form.Form):
    user = _get_profile_form_user(frm)
    print(user.options)


def _get_profile_form_user(frm: _form.Form) -> _auth.model.User:
    if frm.get_widget('__odm_ui_model').value != 'user':
        raise ValueError('Invalid model.')

    user = _auth.get_user(uid=frm.get_widget('__odm_ui_entity_id').value)
    if not user:
        raise ValueError('User is not found.')

    return user
