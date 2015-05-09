__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from ..core import assetman

assetman.register_package(__name__)
assetman.add_js(__name__ + '@js/jquery-2.1.4.min.js')