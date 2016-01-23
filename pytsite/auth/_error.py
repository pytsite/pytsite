"""Auth Errors.
"""
from pytsite import events as _events

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class LoginError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _events.fire('pytsite.auth.login_error', exception=self, user=kwargs.get('user'))


class DriverNotRegistered(Exception):
    pass
