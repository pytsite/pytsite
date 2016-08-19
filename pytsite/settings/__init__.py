"""Settings Plugin Init.
"""
# Public API
from ._api import define, get, put
from ._frm import Form

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


# Init wrapper
def _init():
    from pytsite import odm, tpl, lang, router, admin
    from . import _api, _model

    # Language package
    lang.register_package(__name__)

    # Template package and globals
    tpl.register_global('settings_get', _api.get)

    # ODM model
    odm.register_model('setting', _model.Setting)

    # Routing
    router.add_rule(admin.base_path() + '/settings/<uid>', 'pytsite.settings@form')
    router.add_rule(admin.base_path() + '/settings/<uid>/submit', 'pytsite.settings@form_submit', methods='POST')

    # Sidebar section
    admin.sidebar.add_section('settings', __name__ + '@settings', 2000, ('*',))


# Package initialization
_init()
