"""Settings Plugin Functions
"""
from typing import Any as _Any
from pytsite import admin as _admin, router as _router, odm as _odm
from . import _frm

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_settings = {}


def define(uid: str, frm: _frm.Form, menu_title: str, menu_icon: str, permissions: str = '*', menu_weight: int = 0):
    """Define setting.
    """
    if uid in _settings:
        raise KeyError("Setting '{}' already defined.".format(uid))

    _settings[uid] = {
        'title': menu_title,
        'form': frm,
        'perm_name': permissions,
    }

    url = _router.ep_path('pytsite.settings@form', {'uid': uid})
    _admin.sidebar.add_menu('settings', uid, menu_title, url, menu_icon, weight=menu_weight, permissions=permissions)


def get_definition(uid: str) -> dict:
    """Get setting's definition.
    """
    if uid not in _settings:
        raise KeyError("Setting '{}' is not defined.".format(uid))

    return _settings[uid]


def get(uid: str, default=None) -> _Any:
    """Get setting's value.
    """
    uid_split = uid.split('.')

    if uid_split[0] not in _settings:
        raise KeyError("Setting '{}' is not defined.".format(uid_split[0]))

    entity = _odm.find('setting').eq('uid', uid_split[0]).first()
    if not entity:
        return default if default is not None else {}

    setting_value = entity.f_get('value')
    if len(uid_split) == 2:
        return setting_value.get(uid_split[1]) or default  # 'or' is important here because value can contain None!
    else:
        return setting_value


def put(uid: str, value: _Any):
    """Set setting's value.
    """
    uid_split = uid.split('.')

    if uid_split[0] not in _settings:
        raise KeyError("Setting '{}' is not defined.".format(uid_split[0]))

    entity = _odm.find('setting').eq('uid', uid_split[0]).first()
    if not entity:
        entity = _odm.dispense('setting').f_set('uid', uid_split[0])

    with entity:
        stored_value = dict(entity.f_get('value'))
        if len(uid_split) == 2:
            stored_value[uid_split[1]] = value
            entity.f_set('value', stored_value)
        else:
            entity.f_set('value', value)

        entity.save()
