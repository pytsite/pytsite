"""JS API.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


__import__('pytsite.jquery')

from pytsite.core import router, assetman


router.add_rule('/js_api/<string:endpoint>', 'pytsite.js_api.endpoints.request', methods=['GET', 'POST'])

assetman.register_package(__name__)
assetman.add_js('pytsite.js_api@js/common.js')
