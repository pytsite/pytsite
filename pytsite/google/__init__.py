"""PytSite Google Init.
"""
# Public API
from . import _widget as widget
from ._api import get_map_link

# Necessary libraries
import re as _re
from pytsite import reg as _reg, browser as _browser, assetman as _assetman, lang as _lang

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


__maps_url_re = _re.compile('^https://maps.googleapis.com/maps/api/js')
__libraries_re = _re.compile('libraries=([a-z]+)')


def __browser_library_maps_callback(permanent: bool, **kwargs):
    # Google Map API key is required
    api_key = _reg.get('google.maps.key')
    if not api_key:
        raise ValueError("Configuration parameter 'google.maps.key' is not defined. You can obtain it at {}.".
                         format('https://developers.google.com/maps/documentation/javascript/get-api-key'))

    # Search for currently added Google JSs to find which Google libraries included
    asset_weight = 0
    libs = kwargs.get('libraries', [])
    for loc in _assetman.get_locations('js'):
        if __maps_url_re.match(loc[0]) and 'libraries=' in loc[0]:
            # Remember weight of the location to place new one at the same position
            asset_weight = loc[1]

            # Extracting Google libraries list
            libs += __libraries_re.findall(loc[0])[0].split(',')

    # Remove probably previous added link too Google Maps API JS
    _assetman.remove(__maps_url_re, 'js')

    # Add assets
    libs = ','.join(libs)
    js = 'https://maps.googleapis.com/maps/api/js?libraries={}&amp;language={}&amp;key={}'\
        .format(libs, _lang.get_current(), api_key)

    _assetman.add(js, 'js', asset_weight, permanent)


def __init():
    """Init wrapper.
    """
    _assetman.register_package(__name__)
    _browser.register('google-maps', __browser_library_maps_callback)


__init()
