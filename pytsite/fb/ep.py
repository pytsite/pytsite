"""Facebook Endpoints.
"""
from pytsite import router as _router, http as _http
from ._session import AuthSession as _AuthSession

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def authorize(args: dict, inp: dict):
    """Authorization endpoint.
    """
    # Checking for errors
    error = inp.get('error_description')
    if error:
        _router.session.add_error(error)

    # initializing authorization session
    session = _AuthSession(inp.get('state'))

    return _http.response.Redirect(_router.url(session.final_redirect_uri, query=inp))
