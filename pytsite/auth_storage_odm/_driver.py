"""PytSIte Authentication ODM Storage Driver.
"""
from typing import Iterable as _Iterable
from pytsite import auth as _auth, odm as _odm
from . import _model

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Driver(_auth.driver.Storage):
    def get_name(self) -> str:
        return 'odm'

    def create_role(self, name: str, description: str = '') -> _auth.model.RoleInterface:
        role = _odm.dispense('role')  # type: _model.Role
        role.name = name
        role.description = description
        role.save()

        return role

    def get_role(self, name: str) -> _auth.model.RoleInterface:
        role = _odm.find('role').where('name', '=', name).first()
        if not role:
            raise _auth.error.RoleNotExist("Role '{}' does not exist.".format(name))

        return role

    def get_roles(self) -> _Iterable[_auth.model.RoleInterface]:
        pass

    def create_user(self, login: str, password: str = None) -> _auth.model.UserInterface:
        user = _odm.dispense('user')  # type: _model.User
        user.login = login
        user.email = login
        user.password = password

        if not user.is_anonymous and not user.is_system:
            user.save()

        return user

    def get_user(self, login: str = None, nickname: str = None, access_token: str = None,
                 uid: str = None) -> _auth.model.UserInterface:
        # Don't cache finder results due to frequent user updates in database
        f = _odm.find('user').cache(0)
        if login is not None:
            f.where('login', '=', login)

        elif nickname is not None:
            f.where('nickname', '=', nickname)

        elif access_token is not None:
            f.where('access_token', '=', access_token)

        elif uid is not None:
            f.where('_id', '=', uid)

        else:
            raise RuntimeError('User search criteria was not specified.')

        user = f.first()  # type: _model.User
        if not user:
            raise _auth.error.UserNotExist("User not exist: login={}, nickname={}, access_token={}, uid={}"
                                           .format(login, nickname, access_token, uid))

        return user

    def get_users(self, active_only: bool = True, sort_field: str = None, sort_order: int = 1, limit: int = 0,
                  skip: int = 0, roles: tuple = ()) -> _Iterable[_auth.model.UserInterface]:
        f = _odm.find('user')

        if active_only:
            f.where('status', '=', 'active')

        if sort_field:
            if sort_field in ('created', 'modified'):
                sort_field = '_' + sort_field
            f.sort([(sort_field, sort_order)])

        if roles:
            f.where('roles', 'in', roles)

        if skip:
            f.skip(skip)

        return f.get(limit)
