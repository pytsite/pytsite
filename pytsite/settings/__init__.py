"""PytSite Settings Management
"""
# Public API
from ._api import is_defined, define, get, put, form_url
from ._frm import Form

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import odm, tpl, lang, router, admin, permissions, events
    from . import _api, _model, _controllers, _frm, _eh

    # Resources
    lang.register_package(__name__)
    tpl.register_global('settings_get', _api.get)

    # Lang global to gte application's name from settings
    lang.register_global('app@app_name', lambda language, args: get('app.app_name_' + language, 'PytSite'))

    # ODM model
    odm.register_model('setting', _model.Setting)

    # Routing
    router.handle(_controllers.Form(), admin.base_path() + '/settings/<uid>', 'pytsite.settings@form')

    # Admin sidebar section
    admin.sidebar.add_section('settings', __name__ + '@settings', 2000, sort_items_by='title')

    # Define default application settings form
    permissions.define_permission('app.settings.manage', __name__ + '@manage_app_settings', 'app')
    define('app', _frm.Application, __name__ + '@application', 'fa fa-cube', 'app.settings.manage')

    # Event handlers
    router.on_dispatch(_eh.on_dispatch)
    events.listen('pytsite.update.4_0_0', _eh.on_update_4_0_0)


_init()
