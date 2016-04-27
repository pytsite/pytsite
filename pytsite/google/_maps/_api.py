"""Geo Functions.
"""
from pytsite import router as _router
from . import _geocoding

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def map_link(lng: float, lat: float, query: str = None, zoom: int = 15) -> str:
    """Get link to th Google map.
    """
    if query:
        return _router.url('https://www.google.com/maps/search/{}/@{},{},{}z'.format(query, lat, lng, zoom))
    else:
        return _router.url('https://www.google.com/maps', query={
            'q': '{},{}'.format(lat, lng)
        })


def encode(address: str, **kwargs):
    return _geocoding.GeoCoder().encode(address, **kwargs)


def decode(lng: float, lat: float, **kwargs):
    return _geocoding.GeoCoder().decode(lng, lat, **kwargs)
