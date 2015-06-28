"""Pytsite ODM UI.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    # Dependencies
    __import__('pytsite.auth')
    __import__('pytsite.admin')

    from pytsite.core import router, tpl, assetman, lang, events
    from . import _event_handlers
    from ._model import UIMixin

    # Browse
    router.add_rule('/admin/odm/<string:model>',
                    'pytsite.odm_ui.eps.browse',
                    filters=('pytsite.auth.eps.filter_authorize',))
    router.add_rule('/admin/odm/get_browser_rows/<string:model>',
                    'pytsite.odm_ui.eps.get_browser_rows',
                    filters=('pytsite.auth.eps.filter_authorize',))

    # Create/modify
    router.add_rule('/admin/odm/<string:model>/modify/<string:id>',
                    'pytsite.odm_ui.eps.get_m_form',
                    filters=('pytsite.auth.eps.filter_authorize',))
    router.add_rule('/admin/odm/<string:model>/modify/<string:id>/submit',
                    'pytsite.odm_ui.eps.post_m_form', methods=('POST',),
                    filters=('pytsite.auth.eps.filter_authorize',))

    # Delete
    router.add_rule('/admin/odm/<string:model>/delete',
                    'pytsite.odm_ui.eps.get_d_form',
                    filters=('pytsite.auth.eps.filter_authorize',))
    router.add_rule('/admin/odm/<string:model>/delete/submit',
                    'pytsite.odm_ui.eps.post_d_form',methods=('POST',),
                    filters=('pytsite.auth.eps.filter_authorize',))

    lang.register_package(__name__)
    tpl.register_package(__name__)
    assetman.register_package(__name__)

    events.listen('pytsite.core.odm@register_model', _event_handlers.odm_register_model)

__init()


# Public API
from . import _functions, _model, _widget as widget
UIMixin = _model.UIMixin
get_m_form = _functions.get_m_form
