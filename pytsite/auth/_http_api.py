"""PytSite Auth HTTP API.
"""
from pytsite import http as _http, events as _events, util as _util
from . import _api, _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _get_access_token_info(token: str) -> dict:
    r = _api.get_access_token_info(token)
    r.update({
        'token': token,
        'created': _util.w3c_datetime_str(r['created']),
        'expires': _util.w3c_datetime_str(r['expires']),
    })

    return r


def post_access_token(inp: dict) -> dict:
    """Sign in user.
    """
    try:
        # Try to sign in user via driver
        user = _api.sign_in(inp.get('driver'), inp)

        return _get_access_token_info(_api.generate_access_token(user))

    except _error.AuthenticationError as e:
        raise _http.error.Unauthorized(str(e))


def get_access_token(inp: dict, token: str) -> dict:
    """Get information about user's access token.
    """
    try:
        return _get_access_token_info(token)

    except _error.InvalidAccessToken as e:
        raise _http.error.Unauthorized(str(e))


def delete_access_token(inp: dict, token: str) -> dict:
    """Sign out user.
    """
    try:
        _api.sign_out(_api.get_current_user())
        _api.revoke_access_token(token)

        return {'status': True}

    except (_error.UserNotExist, _error.InvalidAccessToken) as e:
        raise _http.error.Unauthorized(str(e))


def get_user(inp: dict, uid: str) -> dict:
    """Get information about user.
    """
    if _api.get_current_user().is_anonymous:
        raise _http.error.Forbidden('Authentication required')

    try:
        user = _api.get_user(uid=uid)

    except _error.UserNotExist:
        raise _http.error.Unauthorized()

    r = user.as_jsonable()

    _events.fire('pytsite.auth.http_api.get_user', user=user, response=r)

    return r


def patch_user(inp: dict, uid: str) -> dict:
    """Update user.
    """
    allowed_fields = ('login', 'email', 'password', 'nickname', 'first_name', 'last_name', 'description', 'birth_date',
                      'gender', 'phone', 'urls', 'profile_is_public', 'country', 'city')
    c_user = _api.get_current_user()

    # Check permissions
    if c_user.is_anonymous:
        raise _http.error.Forbidden('Authentication required')

    raise NotImplementedError('Not implemented yet')


def patch_follow(inp: dict, **kwargs) -> bool:
    """Follow.
    """
    op = kwargs.get('op')  # What to do: follow or unfollow
    uid = kwargs.get('uid')  # Who to (un)follow

    # Does all required arguments present?
    if not op or not uid:
        raise _http.error.InternalServerError('Insufficient arguments.')

    # Is current user authorized
    current_user = _api.get_current_user()
    if current_user.is_anonymous:
        raise _http.error.Unauthorized()

    # Load user
    user = _api.get_user(uid=uid)

    if op == 'follow':
        _api.switch_user_to_system()
        user.add_follower(current_user).save()
        current_user.add_follows(user).save()
        _api.restore_user()

        _events.fire('pytsite.auth.follow', user=user, follower=current_user)

        return True

    elif op == 'unfollow':
        _api.switch_user_to_system()
        user.remove_follower(current_user).save()
        current_user.remove_follows(user).save()
        _api.restore_user()

        _events.fire('pytsite.auth.unfollow', user=user, follower=current_user)

        return True

    else:
        raise _http.error.InternalServerError("Invalid operation: 'follow' or 'unfollow' expected.")
