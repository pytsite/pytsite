__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core import assetman

assetman.register_package(__name__)
assetman.add_css(__name__ + '@bootstrap/css/bootstrap.min.css')
assetman.add_css(__name__ + '@font-awesome/css/font-awesome.min.css')
assetman.add_js(__name__ + '@bootstrap/js/bootstrap.min.js')
