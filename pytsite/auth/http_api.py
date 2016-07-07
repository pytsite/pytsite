"""PytSite Auth HTTP API.
"""
from pytsite import http as _http, events as _events, util as _util, assetman as _assetman
from . import _api, _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def post_sign_in(inp: dict) -> dict:
    """Sign in user.
    """
    try:
        # Try to sign in user via driver
        return {'access_token': _api.sign_in(inp.get('driver'), inp).access_token}

    except _error.AuthenticationError as e:
        raise _http.error.Unauthorized(str(e))


def post_sign_out(inp: dict) -> dict:
    """Sign out user.
    """
    try:
        _api.sign_out(_api.current_user())

    except _error.UserNotExist as e:
        raise _http.error.Unauthorized(e)


def get_access_token_info(inp: dict) -> dict:
    """Get information about user's access token.
    """
    try:
        return _api.get_access_token_info(inp.get('access_token', ''))

    except _error.InvalidAccessToken as e:
        raise _http.error.Unauthorized(e)


def get_user(inp: dict) -> dict:
    """Get information about user.
    """
    try:
        current_user = _api.current_user()

        uid = inp.get('uid')
        if uid:
            user = _api.get_user(uid=uid)
        elif not current_user.is_anonymous:
            user = current_user
        else:
            raise RuntimeError('You should either specify the UID or authorize yourself.')

    except _error.UserNotExist:
        raise _http.error.Unauthorized()

    r = {
        'uid': user.uid,
    }

    if user.profile_is_public:
        r.update({
            'profile_url': user.profile_view_url,
            'nickname': user.nickname,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'full_name': user.full_name,
            'birth_date': _util.rfc822_datetime_str(user.birth_date),
            'gender': user.gender,
            'phone': user.phone,
            'follows': [f.uid for f in user.follows],
            'followers': [f.uid for f in user.followers],
            'picture': {
                'url': user.picture.url,
                'width': user.picture.width,
                'height': user.picture.height,
                'length':  user.picture.length,
                'mime':  user.picture.mime,
            },
            'urls': user.urls,
        })

    if current_user.uid == user.uid or current_user.is_admin:
        r.update({
            'created': _util.rfc822_datetime_str(user.created),
            'login': user.login,
            'email': user.email,
            'last_sign_in': _util.rfc822_datetime_str(user.last_sign_in),
            'last_activity': _util.rfc822_datetime_str(user.last_activity),
            'sign_in_count': user.sign_in_count,
            'status': user.status,
            'profile_is_public': user.profile_is_public,
            'roles': [role.name for role in user.roles],
        })

    _events.fire('pytsite.auth.http_api.get_user', user=user, response=r)

    return r


def patch_follow(inp: dict) -> bool:
    """Follow.
    """
    op = inp.get('op')
    uid = inp.get('uid')

    # Does all required arguments present?
    if not op or not uid:
        raise _http.error.InternalServerError('Insufficient arguments.')

    # Is current user authorized
    current_user = _api.current_user()
    if current_user.is_anonymous:
        raise _http.error.Unauthorized()

    user = _api.get_user(uid=inp.get('uid'))

    if op == 'follow':
        _api.switch_user(user)
        user.add_follower(current_user)
        user.save()
        _api.switch_user(current_user)

        current_user.add_follows(user)
        current_user.save()

        _events.fire('pytsite.auth.follow', user=user, follower=current_user)

        return True

    elif op == 'unfollow':
        _api.switch_user(user)
        user.remove_follower(current_user)
        user.save()
        _api.switch_user(current_user)

        current_user.remove_follows(user)
        current_user.save()

        _events.fire('pytsite.auth.unfollow', user=user, follower=current_user)

        return True

    else:
        raise _http.error.InternalServerError('Operation type must be specified.')


def get_login_form(inp: dict) -> dict:
    frm = _api.get_sign_in_form(
        auth_driver_name=inp.get('driver'),
        uid=inp.get('uid'),
        title=inp.get('title'),
        css=inp.get('css', ''),
        modal=inp.get('modal', False)
    )

    return {
        'form': _util.minify_html(frm.render()),
        '_css': _assetman.get_urls('css'),
        '_js': _assetman.get_urls('js')
    }


def get_is_anonymous(inp: dict) -> bool:
    return _api.current_user().is_anonymous
