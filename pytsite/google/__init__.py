"""PytSite Google Init.
"""
# Public API
from . import _maps as maps

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _browser_library_maps() -> list:
    from pytsite import reg, lang, router

    # Google Map API key is required
    api_key = reg.get('google.maps.client_key')
    if not api_key:
        raise RuntimeError("Configuration parameter 'google.maps.client_key' is not defined. Obtain it at {}.".
                           format('https://developers.google.com/maps/documentation/javascript/get-api-key'))

    google_url = router.url('https://maps.googleapis.com/maps/api/js', query={
        'language': lang.get_current(),
        'key': api_key,
        'callback': 'pytsite.google.maps.initCallback',
    })

    libs = ','.join(reg.get('google.maps.libraries', []))
    if libs:
        google_url = router.url(google_url, query={'libraries': libs})

    return [
        'pytsite.google@js/common.js',
        'pytsite.google@js/maps.js',
        'pytsite.google@css/maps.css',
        (google_url, 'js', True, True),
    ]


def _browser_library_platform() -> list:
    return [
        'pytsite.google@js/common.js',
        'pytsite.google@js/platform.js',
        ('https://apis.google.com/js/platform.js?onload=pytsiteGooglePlatformInitCallback', 'js', True, True)
    ]


def _init():
    """Init wrapper.
    """
    from pytsite import browser, assetman

    assetman.register_package(__name__)
    browser.register('google-maps', _browser_library_maps)
    browser.register('google-platform', _browser_library_platform)


_init()
