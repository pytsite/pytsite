"""PytSite HTTP API Event Handlers.
"""
from pytsite import reg as _reg, metatag as _metatag, http as _http

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def router_dispatch():
    _metatag.t_set('pytsite-http-api-version', _reg.get('http_api.version', 1))


def router_response(response: _http.response.Response):
    # No cookies in responses from HTTP API
    if 'PytSite-HTTP-API' in response.headers:
        response.headers.remove('Set-Cookie')
