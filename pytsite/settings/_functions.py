"""Settings Plugin Functions.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core import router as _router, form as _form
from pytsite import admin

__settings = {}


def define_setting(uid: str, form: _form.Base, menu_title: str, menu_icon: str, menu_weight: int=0):
    if uid in __settings:
        raise KeyError("Setting '{}' already defined.".format(uid))

    __settings[uid] = {'title': menu_title,  'form': form, 'weight': menu_weight}

    url = _router.endpoint_url('pytsite.settings.eps.form', {'uid': uid})
    admin.sidebar.add_menu('settings', uid, menu_title, url, menu_icon, permissions=('*',))

def get_setting(uid: str):
    if uid not in __settings:
        raise KeyError("Setting '{}' is not defined.".format(uid))

    return __settings[uid]
