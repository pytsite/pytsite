"""PytSite Auth HTTP API
"""
from pytsite import auth as _auth, router as _router, http as _http

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def http_api_pre_request():
    # Authorize user by access token
    access_token = _router.request().headers.get('PytSite-Auth')

    if not access_token:
        return

    try:
        _auth.switch_user(_auth.get_user(access_token=access_token))
        _auth.prolong_access_token(access_token)

    except (_auth.error.InvalidAccessToken, _auth.error.UserNotExist, _auth.error.AuthenticationError) as e:
        raise _http.error.Forbidden(response=_http.response.JSON({'error': str(e)}))
