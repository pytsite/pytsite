__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core import assetman

assetman.register_package(__name__)
assetman.add_css(__name__ + '@css/bootstrap.min.css')
assetman.add_js(__name__ + '@js/bootstrap.min.js')
