"""PytSite Geo IP Package.
"""
# Public API
from . import _model as model, _error as error

from pytsite import odm as _odm


# Public API
from ._api import resolve

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


_odm.register_model('geo_ip', model.GeoIP)
