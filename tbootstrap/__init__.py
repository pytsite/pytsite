__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from ..core import assetman
from .. import jquery

assetman.register_package(__name__)
assetman.add_css(__name__ + '@css/bootstrap.min.css')
assetman.add_js(__name__ + '@js/bootstrap.min.js')