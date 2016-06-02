"""PytSite Auth HTTP API.
"""
from pytsite import http as _http, auth as _auth

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def any_post_sign_in(inp: dict):
    try:
        driver = _auth.get_driver(inp.get('driver'))
        print(driver)

    except _auth.error.AuthenticationError:
        raise _http.error.Unauthorized('Authorization error.')
