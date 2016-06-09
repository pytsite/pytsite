"""PytSite Auth HTTP API.
"""
from pytsite import http as _http, auth as _auth

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def post_sign_in(inp: dict) -> dict:
    try:
        # Try to sign in user via driver
        user = _auth.sign_in(inp.get('driver'), inp)

        fields = ['access_token'] + [f.strip() for f in inp.get('fields', '').split(',')]
        r = user.as_dict(fields)
        r['access_token_ttl'] = _auth.get_access_token_info(user.access_token)['ttl']

        return {'access_token': user.access_token}

    except _auth.error.AuthenticationError as e:
        raise _http.error.Unauthorized(str(e))


def post_sign_out(inp: dict) -> dict:
    try:
        _auth.sign_out(_auth.sign_in_by_token(inp.get('access_token', '')))
    except _auth.error.AuthenticationError as e:
        raise _http.error.Unauthorized(str(e))


def get_access_token_info(inp: dict) -> dict:
    try:
        return _auth.get_access_token_info(inp.get('access_token', ''))

    except _auth.error.InvalidAccessToken as e:
        raise _http.error.Unauthorized(e)


def get_user(inp: dict) -> dict:
    user = _auth.sign_in_by_token(inp.get('access_token', ''))

    return user.as_dict(['login'] + [f.strip() for f in inp.get('fields', '').split(',')])
