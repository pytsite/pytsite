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

    abp = admin.base_path()
    auth_filter = 'pytsite.auth@f_authorize'

    # Route: ODM browser page
    router.add_rule(abp + '/odm_ui/<model>', 'pytsite.odm_ui@browse', filters=auth_filter)

    # Route: get ODM browser table rows
    router.add_rule(abp + '/odm_ui/browse_get_rows/<model>', 'pytsite.odm_ui@browse_get_rows', filters=auth_filter)

    # Route: 'create/modify' ODM entity form show
    router.add_rule(abp + '/odm_ui/<model>/modify/<id>', 'pytsite.odm_ui@m_form', filters=auth_filter)

    # Route: 'create/modify' ODM entity form submit
    # IMPORTANT: admin path prefix is not used here.
    router.add_rule('/odm_ui/<model>/modify/<id>/submit', 'pytsite.odm_ui@m_form_submit', methods='POST',
                    filters=auth_filter)

    # Route: 'delete' form show
    router.add_rule(abp + '/odm_ui/<model>/delete', 'pytsite.odm_ui@d_form', filters=auth_filter)

    # Route: 'delete' form submit
    # IMPORTANT: admin path prefix is not used here.
    router.add_rule('/odm_ui/<model>/delete/submit', 'pytsite.odm_ui@d_form_submit', filters=auth_filter)

    # Resources
    lang.register_package(__name__)
    tpl.register_package(__name__)
    assetman.register_package(__name__)
    http_api.register_package('odm_ui', 'pytsite.odm_ui.http_api')


_init()
