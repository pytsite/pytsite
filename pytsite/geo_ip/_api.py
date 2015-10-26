"""PytSite Geo IP Functions.
"""
import requests as _requests
import re as _re
from pytsite import odm as _odm

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


_private_ip_re = _re.compile('(127\.|10\.|172\.(16|17|18|19|20|21|22|23|24|25|26|27|28|29|30|31|32)|192\.168\.)')


def resolve(ip: str) -> dict:
    """Get data about an IP address.
    """
    entity = _odm.find('geo_ip').where('ip', '=', ip).first()

    if not entity:
        entity = _odm.dispense('geo_ip').f_set('ip', ip)
        if not _private_ip_re.match(ip):
            r = _requests.get('http://www.telize.com/geoip/{}'.format(ip))
            if r.status_code != 200:
                raise Exception(r.text)

            for f_name, f_val in r.json().items():
                if f_name not in ('offset',):
                    entity.f_set(f_name, f_val)

        entity.save()

    return entity
