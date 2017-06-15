"""PytSite Settings Package.
"""
# Public API
from ._api import is_defined, define, get, put, form_url
from ._frm import Form

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import odm, tpl, lang, router, admin
    from . import _api, _model, _controllers

    # Resources
    lang.register_package(__name__)
    tpl.register_global('settings_get', _api.get)

    # ODM model
    odm.register_model('setting', _model.Setting)

    # Routing
    router.handle(_controllers.Form(), admin.base_path() + '/settings/<uid>', 'pytsite.settings@form')

    # Admin sidebar section
    admin.sidebar.add_section('settings', __name__ + '@settings', 2000, sort_items_by='title')


_init()
