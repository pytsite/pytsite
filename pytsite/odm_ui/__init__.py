"""Pytsite ODM UI.
"""
# Public API
from . import _functions, _widget as widget
from ._model import UIMixin, Model
get_m_form = _functions.get_m_form
check_permissions = _functions.check_permissions


__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

# Dependencies
__import__('pytsite.auth')
__import__('pytsite.admin')


def __init():
    from pytsite import assetman, events, tpl, lang, router, admin
    from . import _event_handlers
    from ._model import UIMixin

    # Browse
    router.add_rule(admin.base_path() + '/odm_ui/<string:model>',
                    'pytsite.odm_ui.ep.browse',
                    filters='pytsite.auth.ep.filter_authorize')
    router.add_rule(admin.base_path() + '/odm_ui/get_browser_rows/<string:model>',
                    'pytsite.odm_ui.ep.get_browser_rows',
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

    events.listen('pytsite.odm.register_model', _event_handlers.odm_register_model)

__init()
