"""PytSite Geo IP Package.
"""
from pytsite import odm as _odm
from ._odm_model import GeoIP as _GeoIPModel

# Public API
from ._api import resolve

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


_odm.register_model('geo_ip', _GeoIPModel)
