"""Settings Plugin Functions
"""
from typing import Callable as _Callable
from pytsite import admin as _admin, auth as _auth, router as _router, odm as _odm, permission as _permission
from . import _frm

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_settings = {}


def define(uid: str, form_widgets_setup: _Callable, menu_title: str, menu_icon: str, menu_weight: int = 0,
           perm_name: str = '*', perm_description: str = None):
    """Define setting.
    """
    if uid in _settings:
        raise KeyError("Setting '{}' already defined.".format(uid))

    _settings[uid] = {
        'title': menu_title,
        'form_widgets_setup': form_widgets_setup,
        'weight': menu_weight,
        'perm_name': perm_name,
        'perm_description': perm_description,
    }

    if perm_name != '*' and perm_description:
        _permission.define_permission(perm_name, perm_description, 'admin')

    url = _router.ep_url('pytsite.settings.ep.form', {'uid': uid})
    _admin.sidebar.add_menu('settings', uid, menu_title, url, menu_icon, permissions=perm_name)


def get_definition(uid: str) -> dict:
    """Get setting definition.
    """
    if uid not in _settings:
        raise KeyError("Setting '{}' is not defined.".format(uid))

    return _settings[uid]


def get_setting(uid) -> dict:
    """Get setting value.
    """
    if uid not in _settings:
        raise KeyError("Setting '{}' is not defined.".format(uid))

    entity = _odm.find('setting').where('uid', '=', uid).first()
    if not entity:
        return {}

    return entity.f_get('value')


def set_setting(uid, value: dict):
    """Set setting value.
    """
    entity = _odm.find('setting').where('uid', '=', uid).first()
    if not entity:
        entity = _odm.dispense('setting').f_set('uid', uid)

    entity.f_set('value', value).save()
