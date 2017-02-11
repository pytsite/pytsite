"""PytSite Geo IP Package.
"""
# Public API
from . import _model as model, _error as error
from ._api import resolve

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    from pytsite import odm, events, cron
    from . import _eh

    odm.register_model('geo_ip', model.GeoIP)

    cron.weekly(_eh.cron_weekly)
    events.listen('pytsite.update', _eh.pytsite_update)


__init()
