"""PytSite Geo IP Package.
"""
# Public API
from . import _model as model, _error as error
from ._api import resolve


__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    from pytsite import odm, events
    from . import eh

    odm.register_model('geo_ip', model.GeoIP)

    events.listen('pytsite.cron.weekly', eh.pytsite_cron_weekly)
    events.listen('pytsite.update', eh.pytsite_update)


__init()
