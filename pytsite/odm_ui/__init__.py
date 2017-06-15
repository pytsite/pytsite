"""PytSite ODM UI.
"""
# Public API
from . import _widget as widget, _forms as forms, _model as model
from ._browser import Browser
from ._api import get_m_form, get_d_form, get_model_class

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import assetman, tpl, lang, router, admin, http_api
    from . import _controllers, _http_api_controllers

    abp = admin.base_path()
    auth_filter = 'pytsite.auth@authorize'

    # Route: ODM browser page
    router.handle(_controllers.Browse(), abp + '/odm_ui/<model>', 'pytsite.odm_ui@browse', filters=auth_filter)

    # Route: 'create/modify' ODM entity form display
    router.handle(_controllers.ModifyForm(), abp + '/odm_ui/<model>/modify/<eid>', 'pytsite.odm_ui@m_form',
                  filters=auth_filter)

    # Route: 'delete' form display
    router.handle(_controllers.DeleteForm(), abp + '/odm_ui/<model>/delete', 'pytsite.odm_ui@d_form',
                  methods=('GET', 'POST'), filters=auth_filter)

    # Resources
    lang.register_package(__name__)
    tpl.register_package(__name__)

    assetman.register_package(__name__)
    assetman.t_js(__name__ + '@**/*.js')

    # HTTP API handlers
    http_api.handle('GET', 'odm_ui/rows/<model>', _http_api_controllers.GetRows(), 'pytsite.odm_ui@get_rows')


_init()
