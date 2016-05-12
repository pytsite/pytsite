"""PytSite Google Init.
"""
# Public API
from . import _maps as maps

# Necessary imports
from pytsite import reg as _reg, browser as _browser, assetman as _assetman, lang as _lang, router as _router

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _browser_library_maps() -> list:
    # Google Map API key is required
    api_key = _reg.get('google.maps.client_key')
    if not api_key:
        raise RuntimeError("Configuration parameter 'google.maps.client_key' is not defined. Obtain it at {}.".
                           format('https://developers.google.com/maps/documentation/javascript/get-api-key'))

    google_url = _router.url('https://maps.googleapis.com/maps/api/js', query={
        'language': _lang.get_current(),
        'key': api_key,
        'callback': 'pytsite.google.maps.initCallback'
    })

    libs = ','.join(_reg.get('google.maps.libraries', []))
    if libs:
        google_url = _router.url(google_url, query={'libraries': libs})

    return [
        'pytsite.google@js/common.js',
        'pytsite.google@js/maps.js',
        'pytsite.google@css/maps.css',
        (google_url, 'js'),
    ]


def _init():
    """Init wrapper.
    """
    _assetman.register_package(__name__)
    _browser.register('google-maps', _browser_library_maps)


_init()
