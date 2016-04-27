"""PytSite Google Maps Package.
"""
# Public API
from . import _widget as widget, _geocoding as geocoding
from ._api import encode, decode, map_link

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import tpl

    tpl.register_global('google_maps_map_link', map_link)


_init()
