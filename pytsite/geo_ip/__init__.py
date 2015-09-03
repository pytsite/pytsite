"""PytSite Geo IP Package.
"""
# Public API
from . import _odm_model as odm_model, _error as error

from pytsite import odm as _odm


# Public API
from ._api import resolve

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


_odm.register_model('geo_ip', odm_model.GeoIP)
