"""PytSite Auth HTTP API.
"""
from pytsite import events as _events, util as _util, logger as _logger, routing as _routing
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


class PostAccessToken(_routing.Controller):
    """Create access token
    """

    def exec(self) -> dict:
        try:
            # Try to sign in user via driver
            user = _api.sign_in(self.arg('driver'), dict(self.args))

            return _get_access_token_info(_api.generate_access_token(user))

        except (_error.AuthenticationError, _error.UserNotExist) as e:
            _logger.warn(e)
            raise self.forbidden()


class GetAccessToken(_routing.Controller):
    """Get information about user's access token
    """

    def exec(self) -> dict:
        try:
            return _get_access_token_info(self.arg('token'))

        except _error.InvalidAccessToken as e:
            raise self.forbidden(str(e))


class DeleteAccessToken(_routing.Controller):
    """Delete access token
    """

    def exec(self) -> dict:
        try:
            _api.sign_out(_api.get_current_user())
            _api.revoke_access_token(self.arg('token'))

            return {'status': True}

        except (_error.UserNotExist, _error.InvalidAccessToken) as e:
            raise self.forbidden(str(e))


class IsAnonymous(_routing.Controller):
    """Check if the current user is anonymous
    """

    def exec(self):
        return _api.get_current_user().is_anonymous


class GetUser(_routing.Controller):
    """Get information about user
    """

    def exec(self) -> dict:
        try:
            user = _api.get_user(uid=self.arg('uid'))
            r = user.as_jsonable()
            _events.fire('pytsite.auth.http_api.get_user', user=user, response=r)

            return r

        except _error.UserNotExist:
            raise self.forbidden()


class PatchUser(_routing.Controller):
    """Update user.
    """

    def exec(self) -> dict:
        c_user = _api.get_current_user()

        # Anonymous users cannot manage themselves
        if c_user.is_anonymous:
            raise self.forbidden()

        allowed_fields = ('email', 'nickname', 'first_name', 'last_name', 'description', 'birth_date',
                          'gender', 'phone', 'urls', 'profile_is_public', 'country', 'city')

        return {}


class PostFollow(_routing.Controller):
    """Follow user.
    """

    def exec(self) -> dict:
        # Is current user authorized
        current_user = _api.get_current_user()
        if current_user.is_anonymous:
            raise self.forbidden()

        # Load user to follow
        user = _api.get_user(uid=self.arg('uid'))

        _api.switch_user_to_system()
        user.add_follower(current_user).save()
        current_user.add_follows(user).save()
        _api.restore_user()

        _events.fire('pytsite.auth.follow', user=user, follower=current_user)

        return {'follows': current_user.as_jsonable()['follows']}


class DeleteFollow(_routing.Controller):
    """Unfollow user.
    """

    def exec(self) -> dict:
        # Is current user authorized
        current_user = _api.get_current_user()
        if current_user.is_anonymous:
            raise self.forbidden()

        # Load user to unfollow
        user = _api.get_user(uid=self.arg('uid'))

        _api.switch_user_to_system()
        user.remove_follower(current_user).save()
        current_user.remove_follows(user).save()
        _api.restore_user()

        _events.fire('pytsite.auth.unfollow', user=user, follower=current_user)

        return {'follows': current_user.as_jsonable()['follows']}
