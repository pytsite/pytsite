"""PytSite Geo IP
"""
# Public API
from . import _model as model, _error as error
from ._api import resolve

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import odm, cron
    from . import _eh

    odm.register_model('geo_ip', model.GeoIP)

    cron.weekly(_eh.cron_weekly)


_init()
