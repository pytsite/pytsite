"""PytSite ODM UI.
"""
# Public API
from . import _widget as widget, _forms as forms
from ._browser import Browser
from ._api import get_m_form, get_d_form, check_permissions, get_model_class
from ._entity import UIMixin, UIEntity

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    from pytsite import assetman, events, tpl, lang, router, admin, ajax
    from . import _eh

    abp = admin.base_path()
    auth_filter = 'pytsite.auth.ep.filter_authorize'

    # Route: ODM browser page
    router.add_rule(abp + '/odm_ui/<string:model>', 'pytsite.odm_ui.ep.browse', filters=auth_filter)

    # Route: get ODM browser table rows
    router.add_rule(abp + '/odm_ui/browse_get_rows/<string:model>', 'pytsite.odm_ui.ep.browse_get_rows',
                    filters=auth_filter)

    # Route: 'create/modify' ODM entity form show
    router.add_rule(abp + '/odm_ui/<string:model>/modify/<string:id>', 'pytsite.odm_ui.ep.m_form',
                    filters=auth_filter)

    # Route: 'create/modify' ODM entity form submit
    router.add_rule(abp + '/odm_ui/<string:model>/modify/<string:id>/submit', 'pytsite.odm_ui.ep.m_form_submit',
                    methods='POST', filters=auth_filter)

    # Route: 'delete' form show
    router.add_rule(abp + '/odm_ui/<string:model>/delete', 'pytsite.odm_ui.ep.d_form', filters=auth_filter)

    # Route: 'delete' form submit
    router.add_rule(abp + '/odm_ui/<string:model>/delete/submit', 'pytsite.odm_ui.ep.d_form_submit', filters=auth_filter)

    # Resources
    lang.register_package(__name__)
    tpl.register_package(__name__)
    assetman.register_package(__name__)

    # Event listeners
    events.listen('pytsite.odm.register_model', _eh.odm_register_model)

    # AJAX form validator
    ajax.register_ep('pytsite.odm_ui.ep.validate_m_form')

__init()
