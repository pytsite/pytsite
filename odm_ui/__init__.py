"""ODM UI.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

# Dependencies
__import__('pytsite.auth')
__import__('pytsite.js_api')

from pytsite.core import router, lang, tpl, assetman

router.add_rule('/admin/odm/browse/<string:model>',
                'pytsite.odm_ui.endpoints.browse', methods=['GET'])
router.add_rule('/admin/odm/modify/<string:model>/<string:id>',
                'pytsite.odm_ui.endpoints.get_modify_form', methods=['GET'])
router.add_rule('/admin/odm/modify/<string:model>/<string:id>/submit',
                'pytsite.odm_ui.endpoints.post_modify_form', methods=['POST'])
router.add_rule('/admin/odm/delete/<string:model>',
                'pytsite.odm_ui.endpoints.get_delete_form', methods=['GET'])
router.add_rule('/admin/odm/delete/<string:model>/submit',
                'pytsite.odm_ui.endpoints.post_delete_form', methods=['POST'])

lang.register_package(__name__)
tpl.register_package(__name__)
assetman.register_package(__name__)
