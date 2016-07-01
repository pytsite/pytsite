"""Auth Errors.
"""
from pytsite import events as _events

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class AuthenticationError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _events.fire('pytsite.auth.sign_in_error', exception=self, user=kwargs.get('user'))


class DriverNotRegistered(Exception):
    pass


class RoleNotExist(Exception):
    pass


class RoleExists(Exception):
    pass


class UserNotExist(Exception):
    pass


class UserExists(Exception):
    pass


class InvalidAccessToken(Exception):
    pass


class UserModifyForbidden(Exception):
    pass


class UserDeleteForbidden(Exception):
    pass


class RoleModifyForbidden(Exception):
    pass


class RoleDeleteForbidden(Exception):
    pass


class NoAdminUser(Exception):
    pass
