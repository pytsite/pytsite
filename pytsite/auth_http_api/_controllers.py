"""PytSite Auth HTTP API
"""
from typing import Union as _Union
from pytsite import events as _events, util as _util, logger as _logger, routing as _routing, \
    formatters as _formatters, validation as _validation, auth as _auth

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _get_access_token_info(token: str) -> dict:
    r = _auth.get_access_token_info(token)
    r.update({
        'token': token,
        'created': _util.w3c_datetime_str(r['created']),
        'expires': _util.w3c_datetime_str(r['expires']),
    })

    return r


def _get_user_jsonable(user: _auth.model.AbstractUser, current_user: _auth.model.AbstractUser, http_api_version: int):
    jsonable = user.as_jsonable()

    # HTTP API version 1
    if http_api_version == 1:
        if user.profile_is_public or current_user == user or current_user.is_admin:
            jsonable['follows'] = [f.uid for f in user.follows]
            jsonable['followers'] = [f.uid for f in user.followers]

        if current_user == user or current_user.is_admin:
            jsonable['blocked_users'] = [u.uid for u in user.blocked_users]

    return jsonable


class PostAccessToken(_routing.Controller):
    """Issue a new access token
    """

    def exec(self) -> dict:
        try:
            # Try to sign in user via driver
            user = _auth.sign_in(self.arg('driver'), dict(self.args))

            return _get_access_token_info(_auth.generate_access_token(user))

        except (_auth.error.AuthenticationError, _auth.error.UserNotExist) as e:
            _logger.warn(e)
            raise self.forbidden()


class GetAccessToken(_routing.Controller):
    """Get information about an access token
    """

    def exec(self) -> dict:
        try:
            return _get_access_token_info(self.arg('token'))

        except _auth.error.InvalidAccessToken as e:
            raise self.forbidden(str(e))


class DeleteAccessToken(_routing.Controller):
    """Delete an access token
    """

    def exec(self) -> dict:
        try:
            _auth.sign_out(_auth.get_current_user())
            _auth.revoke_access_token(self.arg('token'))

            return {'status': True}

        except (_auth.error.UserNotExist, _auth.error.InvalidAccessToken) as e:
            raise self.forbidden(str(e))


class IsAnonymous(_routing.Controller):
    """Check if the current user is anonymous
    """

    def exec(self) -> _Union[bool, dict]:
        if self.arg('_pytsite_http_api_version') == 1:
            return _auth.get_current_user().is_anonymous

        return {'status': _auth.get_current_user().is_anonymous}


class GetUser(_routing.Controller):
    """Get information about a user
    """

    def exec(self) -> dict:
        try:
            user = _auth.get_user(uid=self.arg('uid'))
            jsonable = _get_user_jsonable(user, _auth.get_current_user(), self.arg('_pytsite_http_api_version'))
            _events.fire('pytsite.auth.http_api.get_user', user=user, json=jsonable)

            return jsonable

        except _auth.error.UserNotExist:
            raise self.not_found()


class GetUsers(_routing.Controller):
    """Get information about multiple users
    """

    def __init__(self):
        super().__init__()

        self.args.add_formatter('uids', _formatters.JSONArrayToList())

    def exec(self) -> list:
        current_user = _auth.get_current_user()
        r = []

        for uid in self.arg('uids'):
            try:
                user = _auth.get_user(uid=uid)
                json = _get_user_jsonable(user, current_user, self.arg('_pytsite_http_api_version'))
                _events.fire('pytsite.auth.http_api.get_user', user=user, json=json)
                r.append(json)

            except Exception as e:
                # Any exception is ignored due to safety reasons
                _logger.warn(e)

        return r


class PatchUser(_routing.Controller):
    """Update user
    """

    def __init__(self):
        super().__init__()
        self.args.add_formatter('birth_date', _formatters.DateTime())
        self.args.add_formatter('urls', _formatters.JSONArrayToList())
        self.args.add_formatter('profile_is_public', _formatters.Bool())

        self.args.add_validation('email', _validation.rule.DateTime())
        self.args.add_validation('gender', _validation.rule.Choice(options=('m', 'f')))

    def exec(self) -> dict:
        user = _auth.get_current_user()

        # Check permissions
        if user.is_anonymous or (user.uid != self.arg('uid') and not user.is_admin):
            raise self.forbidden()

        allowed_fields = ('email', 'nickname', 'picture', 'first_name', 'last_name', 'description', 'birth_date',
                          'gender', 'phone', 'country', 'city', 'urls', 'profile_is_public')

        for k, v in self.args.items():
            if k in allowed_fields:
                user.set_field(k, v)

        if user.is_modified:
            user.save()

        json = _get_user_jsonable(user, user, self.arg('_pytsite_http_api_version'))

        _events.fire('pytsite.auth.http_api.get_user', user=user, json=json)

        return json


class PostFollow(_routing.Controller):
    """Follow a user
    """

    def exec(self) -> dict:
        # Is current user authorized
        current_user = _auth.get_current_user()
        if current_user.is_anonymous:
            raise self.forbidden()

        # Load user to follow
        try:
            user = _auth.get_user(uid=self.arg('uid'))
        except _auth.error.UserNotExist:
            raise self.not_found()

        _auth.switch_user_to_system()
        current_user.add_follows(user).save()
        _auth.restore_user()

        _events.fire('pytsite.auth.follow', user=user, follower=current_user)

        if self.arg('_pytsite_http_api_version') == 1:
            return {'follows': [u.uid for u in current_user.follows]}
        else:
            return {'status': True}


class DeleteFollow(_routing.Controller):
    """Unfollow a user
    """

    def exec(self) -> dict:
        # Is current user authorized?
        current_user = _auth.get_current_user()
        if current_user.is_anonymous:
            raise self.forbidden()

        # Load user to unfollow
        try:
            user = _auth.get_user(uid=self.arg('uid'))
        except _auth.error.UserNotExist:
            raise self.not_found()

        _auth.switch_user_to_system()
        current_user.remove_follows(user).save()
        _auth.restore_user()

        _events.fire('pytsite.auth.unfollow', user=user, follower=current_user)

        if self.arg('_pytsite_http_api_version') == 1:
            return {'follows': [u.uid for u in current_user.follows]}
        else:
            return {'status': True}


class GetFollowsOrFollowers(_routing.Controller):
    """Get followed users or followers
    """

    def __init__(self):
        super().__init__()

        self.args.add_formatter('skip', _formatters.PositiveInt())
        self.args.add_formatter('count', _formatters.Int(minimum=1, maximum=100))

    def exec(self) -> dict:
        if self.arg('_pytsite_http_api_version') < 2:
            raise self.not_found()

        current_user = _auth.get_current_user()

        try:
            user = _auth.get_user(uid=self.arg('uid'))
        except _auth.error.UserNotExist:
            raise self.not_found()

        if user != current_user and not (current_user.is_admin or user.profile_is_public):
            raise self.forbidden()

        skip = self.arg('skip', 0)
        count = self.arg('count', 10)

        if self.arg('_pytsite_http_api_rule_name') == 'pytsite.auth@get_follows':
            users = [u.as_jsonable() for u in user.get_field('follows', skip=skip, count=count)]
            remains = user.follows_count - (skip + count)
            return {'result': users, 'remains': remains if remains > 0 else 0}
        elif self.arg('_pytsite_http_api_rule_name') == 'pytsite.auth@get_followers':
            users = [u.as_jsonable() for u in user.get_field('followers', skip=skip, count=count)]
            remains = user.followers_count - (skip + count)
            return {'result': users, 'remains': remains if remains > 0 else 0}
        else:
            raise self.not_found()


class GetBlockedUsers(_routing.Controller):
    """Get followed users or followers
    """

    def __init__(self):
        super().__init__()

        self.args.add_formatter('skip', _formatters.PositiveInt())
        self.args.add_formatter('count', _formatters.Int(minimum=1, maximum=100))

    def exec(self):
        if self.arg('_pytsite_http_api_version') < 2:
            raise self.not_found()

        try:
            user = _auth.get_user(uid=self.arg('uid'))
        except _auth.error.UserNotExist:
            raise self.not_found()

        current_user = _auth.get_current_user()

        if current_user.is_anonymous or not (current_user == user or current_user.is_admin):
            raise self.forbidden()

        skip = self.arg('skip', 0)
        count = self.arg('count', 10)
        users = [u.as_jsonable() for u in user.get_field('blocked_users', skip=skip, count=count)]
        remains = user.blocked_users_count - (skip + count)

        return {'result': users, 'remains': remains if remains > 0 else 0}


class PostBlockUser(_routing.Controller):
    """Block a user
    """

    def exec(self) -> dict:
        # Is current user authorized
        current_user = _auth.get_current_user()
        if current_user.is_anonymous:
            raise self.forbidden()

        # Load user to block
        try:
            user = _auth.get_user(uid=self.arg('uid'))
        except _auth.error.UserNotExist:
            raise self.not_found()

        _auth.switch_user_to_system()
        current_user.add_blocked_user(user).save()
        _auth.restore_user()

        _events.fire('pytsite.auth.block_user', user=user, blocker=current_user)

        if self.arg('_pytsite_http_api_version') == 1:
            return {'blocked_users': [u.uid for u in current_user.blocked_users]}
        else:
            return {'status': True}


class DeleteBlockUser(_routing.Controller):
    """Unblock a user
    """

    def exec(self) -> dict:
        # Is current user authorized
        current_user = _auth.get_current_user()
        if current_user.is_anonymous:
            raise self.forbidden()

        # Load user to unblock
        try:
            user = _auth.get_user(uid=self.arg('uid'))
        except _auth.error.UserNotExist:
            raise self.not_found()

        _auth.switch_user_to_system()
        current_user.remove_blocked_user(user).save()
        _auth.restore_user()

        _events.fire('pytsite.auth.unblock_user', user=user, blocker=current_user)

        if self.arg('_pytsite_http_api_version') == 1:
            return {'blocked_users': [u.uid for u in current_user.blocked_users]}
        else:
            return {'status': True}
