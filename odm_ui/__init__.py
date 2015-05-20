"""ODM UI.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

__import__('pytsite.js_api')

from pytsite.core import router
router.add_rule('/admin/odm/browse/<string:model>', 'pytsite.odm_ui.endpoints.browse')
