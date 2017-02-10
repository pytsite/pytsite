"""PytSite HTTP API Event Handlers.
"""
from pytsite import reg as _reg, metatag as _metatag, http as _http, router as _router, auth as _auth

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def router_dispatch():
    # Determine current user based on request's argument
    access_token = _router.request().inp.get('access_token')
    if access_token:
        try:
            _auth.get_user(access_token=access_token)
            _auth.prolong_access_token(access_token)

        except (_auth.error.InvalidAccessToken, _auth.error.UserNotExist) as e:
            raise _http.error.Unauthorized(response=_http.response.JSON({'error': str(e)}))

        except _auth.error.AuthenticationError as e:
            raise _http.error.Forbidden(response=_http.response.JSON({'error': str(e)}))

    _metatag.t_set('pytsite-http-api-version', _reg.get('http_api.version', 1))


def router_response(response: _http.response.Response):
    # No cookies in responses from HTTP API
    if 'PytSite-HTTP-API' in response.headers:
        response.headers.remove('Set-Cookie')
