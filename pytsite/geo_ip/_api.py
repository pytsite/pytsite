"""PytSite Geo IP Functions.
"""
import requests as _requests
from pytsite import odm as _odm

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def resolve(ip: str) -> dict:
    """Get data about an IP address.
    """
    entity = _odm.find('geo_ip').where('ip', '=', ip).first()

    if not entity:
        r = _requests.get('http://www.telize.com/geoip/{}'.format(ip))
        if r.status_code != 200:
            raise Exception(r.text)

        entity = _odm.dispense('geo_ip')
        for f_name, f_val in r.json().items():
            if f_name not in ('offset',):
                entity.f_set(f_name, f_val)

        entity.save()

    return entity
