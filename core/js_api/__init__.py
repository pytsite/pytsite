"""JS API.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


from pytsite.core import router, assetman

assetman.register_package(__name__)
assetman.add_js(__name__ + '@js/jquery-2.1.4.min.js')
assetman.add_js(__name__ + '@js/js_api.js')

router.add_rule('/pytsite/core/js_api/<string:ep>', 'pytsite.core.js_api.eps.request', methods=['GET', 'POST'])
