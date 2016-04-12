"""PytSite Geo IP Functions.
"""
import requests as _requests
import re as _re
from pytsite import odm as _odm
from . import _model, _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


_private_ip_re = _re.compile('(127\.|10\.|172\.(16|17|18|19|20|21|22|23|24|25|26|27|28|29|30|31|32)|192\.168\.)')

# external_api_field: our_field
_field_mapping = {
    'as': 'asn',
    'city': 'city',
    'country': 'country',
    'countryCode': 'country_code',
    'isp': 'isp',
    'lat': 'latitude',
    'lon': 'longitude',
    'org': 'organization',
    'zip': 'postal_code',
    'region': 'region',
    'regionName': 'region_name',
    'timezone': 'timezone',
}


def resolve(ip: str) -> _model.GeoIP:
    """Get data about an IP address.
    """
    # Checking for previously fetched data
    entity = _odm.find('geo_ip').where('ip', '=', ip).first()
    if entity:
        return entity

    # Fetching data
    entity = _odm.dispense('geo_ip').f_set('ip', ip)
    if ip != '0.0.0.0' and not _private_ip_re.match(ip):
        r = _requests.get('http://ip-api.com/json/{}'.format(ip))
        if r.status_code != 200:
            raise _error.ResolveError(r.text)
        for ext_api_f, val in r.json().items():
            if ext_api_f in _field_mapping:
                entity.f_set(_field_mapping[ext_api_f], val)

    return entity.save()
