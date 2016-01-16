"""Pytsite ODM UI.
"""
# Public API
from . import _widget as widget
from ._browser import Browser
from ._api import get_m_form, get_mass_action_form, get_d_form, check_permissions
from ._model import UIMixin, Model

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    from pytsite import assetman, events, tpl, lang, router, admin, browser
    from . import _eh
    from ._model import UIMixin

    # Browse
    router.add_rule(admin.base_path() + '/odm_ui/<string:model>',
                    'pytsite.odm_ui.ep.browse',
                    filters='pytsite.auth.ep.filter_authorize')
    router.add_rule(admin.base_path() + '/odm_ui/ajax_get_browser_rows/<string:model>',
                    'pytsite.odm_ui.ep.ajax_get_browser_rows',
                    filters='pytsite.auth.ep.filter_authorize')

    # Create/modify
    router.add_rule(admin.base_path() + '/odm_ui/<string:model>/modify/<string:id>',
                    'pytsite.odm_ui.ep.get_m_form',
                    filters='pytsite.auth.ep.filter_authorize')
    router.add_rule(admin.base_path() + '/odm_ui/<string:model>/modify/<string:id>/submit',
                    'pytsite.odm_ui.ep.post_m_form', methods='POST',
                    filters='pytsite.auth.ep.filter_authorize')

    # Delete
    router.add_rule(admin.base_path() + '/odm_ui/<string:model>/delete', 'pytsite.odm_ui.ep.get_d_form',
                    filters='pytsite.auth.ep.filter_authorize')
    router.add_rule(admin.base_path() + '/odm_ui/<string:model>/delete/submit', 'pytsite.odm_ui.ep.post_d_form',
                    filters='pytsite.auth.ep.filter_authorize')

    lang.register_package(__name__)
    tpl.register_package(__name__)
    assetman.register_package(__name__)

    events.listen('pytsite.odm.register_model', _eh.odm_register_model)

    browser.register_ep('pytsite.odm_ui.ep.ajax_validate_m_form')

__init()
