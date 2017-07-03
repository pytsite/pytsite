"""PytSite GeoIP Event Handlers.
"""
from datetime import datetime as _datetime, timedelta as _timedelta
from pytsite import odm as _odm

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def cron_weekly():
    """'pytsite.cron.weekly' event handler.
    """
    # Delete expired entities
    f = _odm.find('geo_ip').lte('_created', _datetime.now() - _timedelta(weeks=1))
    for e in f.get():
        with e:
            e.delete()
