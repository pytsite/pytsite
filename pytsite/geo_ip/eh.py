"""PytSite GeoIP Event Handlers.
"""
from datetime import datetime as _datetime, timedelta as _timedelta
from pytsite import odm as _odm, console as _console, db as _db

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def pytsite_update(version: str):
    """'pytsite.update' event handler.
    """
    if version in ('0.59.0', '0.63.0'):
        # Re-create 'geo_ips' collection due to its structure changes
        _db.get_collection('geo_ips').drop()
        _console.print_info("Collection 'geo_ips' will be re-created.")


def pytsite_cron_weekly():
    """'pytsite.cron.weekly' event handler.
    """
    # Delete expired entities
    f = _odm.find('geo_ip').where('_created', '<=', _datetime.now() - _timedelta(weeks=1))
    for e in f.get():
        e.delete()
