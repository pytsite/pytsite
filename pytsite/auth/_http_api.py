"""PytSite Auth HTTP API.
"""
from pytsite import http as _http, events as _events, util as _util, logger as _logger
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


def post_access_token(inp: dict, driver: str) -> dict:
    """Generate access token for user.
    """
    try:
        # Try to sign in user via driver
        user = _api.sign_in(driver, inp)

        return _get_access_token_info(_api.generate_access_token(user))

    except (_error.AuthenticationError, _error.UserNotExist) as e:
        _logger.warn(e)
        raise _http.error.Forbidden()


def get_access_token(inp: dict, token: str) -> dict:
    """Get information about user's access token.
    """
    try:
        return _get_access_token_info(token)

    except _error.InvalidAccessToken as e:
        raise _http.error.Forbidden(str(e))


def delete_access_token(inp: dict, token: str) -> dict:
    """Delete access token.
    """
    try:
        _api.sign_out(_api.get_current_user())
        _api.revoke_access_token(token)

        return {'status': True}

    except (_error.UserNotExist, _error.InvalidAccessToken) as e:
        raise _http.error.Forbidden(str(e))


def is_anonymous(inp: dict) -> bool:
    """Check if the current user is anonymous.
    """
    return _api.get_current_user().is_anonymous


def get_user(inp: dict, uid: str) -> dict:
    """Get information about user.
    """
    try:
        user = _api.get_user(uid=uid)

    except _error.UserNotExist:
        raise _http.error.Forbidden()

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
        raise _http.error.Forbidden()

    raise NotImplementedError('Not implemented yet')


def post_follow(inp: dict, uid: str) -> dict:
    """Follow user.
    """
    # Is current user authorized
    current_user = _api.get_current_user()
    if current_user.is_anonymous:
        raise _http.error.Forbidden()

    # Load user to follow
    user = _api.get_user(uid=uid)

    _api.switch_user_to_system()
    user.add_follower(current_user).save()
    current_user.add_follows(user).save()
    _api.restore_user()

    _events.fire('pytsite.auth.follow', user=user, follower=current_user)

    return {'follows': current_user.as_jsonable()['follows']}


def delete_follow(inp: dict, uid: str) -> dict:
    """Unfollow user.
    """
    # Is current user authorized
    current_user = _api.get_current_user()
    if current_user.is_anonymous:
        raise _http.error.Forbidden()

    # Load user to unfollow
    user = _api.get_user(uid=uid)

    _api.switch_user_to_system()
    user.remove_follower(current_user).save()
    current_user.remove_follows(user).save()
    _api.restore_user()

    _events.fire('pytsite.auth.unfollow', user=user, follower=current_user)

    return {'follows': current_user.as_jsonable()['follows']}
