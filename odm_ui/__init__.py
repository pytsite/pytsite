"""ODM UI.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

# Dependencies
__import__('pytsite.auth')
__import__('pytsite.admin')

from pytsite.core import router, lang, tpl, assetman, events
from . import event_handlers

# Browse
router.add_rule('/admin/odm/browse/<string:model>',
                'pytsite.odm_ui.eps.browse',
                methods=['GET'],
                filters=('pytsite.auth.eps.filter_authorize',))
router.add_rule('/admin/odm/get_browser_rows/<string:model>',
                'pytsite.odm_ui.eps.get_browser_rows',
                methods=['GET'],
                filters=('pytsite.auth.eps.filter_authorize',))

# Create/modify
router.add_rule('/admin/odm/modify/<string:model>/<string:id>',
                'pytsite.odm_ui.eps.get_m_form',
                methods=['GET'],
                filters=('pytsite.auth.eps.filter_authorize',))
router.add_rule('/admin/odm/modify/<string:model>/<string:id>/submit',
                'pytsite.odm_ui.eps.post_m_form',
                methods=['POST'],
                filters=('pytsite.auth.eps.filter_authorize',))

# Delete
router.add_rule('/admin/odm/delete/<string:model>',
                'pytsite.odm_ui.eps.get_d_form',
                methods=['GET'],
                filters=('pytsite.auth.eps.filter_authorize',))
router.add_rule('/admin/odm/delete/<string:model>/submit',
                'pytsite.odm_ui.eps.post_d_form',
                methods=['POST'],
                filters=('pytsite.auth.eps.filter_authorize',))

lang.register_package(__name__)
tpl.register_package(__name__)
assetman.register_package(__name__)

events.listen('pytsite.core.odm@register_model', event_handlers.odm_register_model)