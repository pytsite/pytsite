"""PytSite Authentication ODM Storage Driver.
"""
from typing import Iterable as _Iterable
from pytsite import auth as _auth, odm as _odm, form as _form, odm_ui as _odm_ui
from . import _model

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Driver(_auth.driver.Storage):
    def get_name(self) -> str:
        """Get driver's name.
        """
        return 'odm'

    def create_role(self, name: str, description: str = '') -> _auth.model.AbstractRole:
        """Create a new role.
        """
        role_entity = _odm.dispense('role')  # type: _model.ODMRole
        role_entity.f_set('name', name).f_set('description', description).save()

        return _model.Role(role_entity)

    def get_role(self, name: str = None, uid: str = None) -> _auth.model.AbstractRole:
        f = _odm.find('role')

        if name:
            f.eq('name', name)
        elif uid:
            f.eq('_id', uid)
        else:
            raise RuntimeError("Either role's name or UID should be specified.")

        role_entity = f.first()
        if not role_entity:
            raise _auth.error.RoleNotExist("Role '{}' does not exist.".format(name))

        return _model.Role(role_entity)

    def get_roles(self, flt: dict = None, sort_field: str = None, sort_order: int = 1, limit: int = None,
                  skip: int = 0) -> _Iterable[_auth.model.AbstractRole]:
        f = _odm.find('role')

        if sort_field:
            f.sort([(sort_field, sort_order)])

        if skip:
            f.skip(skip)

        if flt:
            for k, v in flt.items():
                if not f.mock.has_field(k):
                    RuntimeError("Role doesn't have field '{}'.".format(k))

                f.eq(k, v)

        # Return generator
        return (_model.Role(role_entity) for role_entity in f.get(limit))

    def create_user(self, login: str, password: str = None) -> _auth.model.AbstractUser:
        user_entity = _odm.dispense('user')  # type: _model.ODMUser
        user_entity.f_set('login', login).f_set('email', login).f_set('password', password)

        if login not in (_auth.model.SYSTEM_USER_LOGIN, _auth.model.ANONYMOUS_USER_LOGIN):
            user_entity.save()

        return _model.User(user_entity)

    def get_user(self, login: str = None, nickname: str = None, access_token: str = None,
                 uid: str = None) -> _auth.model.AbstractUser:

        # Don't cache finder results due to frequent user updates in database
        f = _odm.find('user').cache(0)
        if login is not None:
            f.eq('login', login)
        elif nickname is not None:
            f.eq('nickname', nickname)
        elif access_token is not None:
            f.eq('acs_token', access_token)
        elif uid is not None:
            f.eq('_id', uid)
        else:
            raise RuntimeError('User search criteria was not specified.')

        user_entity = f.first()  # type: _model.ODMUser
        if not user_entity:
            raise _auth.error.UserNotExist("User not exist: login={}, nickname={}, access_token={}, uid={}"
                                           .format(login, nickname, access_token, uid))

        return _model.User(user_entity)

    def get_users(self, flt: dict = None, sort_field: str = None, sort_order: int = 1, limit: int = None,
                  skip: int = 0) -> _Iterable[_auth.model.AbstractUser]:
        f = _odm.find('user')

        if sort_field:
            if sort_field in ('created', 'modified'):
                sort_field = '_' + sort_field
            elif sort_field == 'full_name':
                sort_field = 'first_name'
            elif sort_field == 'is_online':
                sort_field = 'last_activity'
            f.sort([(sort_field, sort_order)])

        if skip:
            f.skip(skip)

        if flt:
            for k, v in flt.items():
                if not f.mock.has_field(k):
                    RuntimeError("User doesn't have field '{}'.".format(k))

                if isinstance(v, (tuple, list)):
                    f.inc(k, v)
                else:
                    f.eq(k, v)

        # Return generator
        return (_model.User(user_entity) for user_entity in f.get(limit))

    def count_users(self, flt: dict = None) -> int:
        f = _odm.find('user')
        if flt:
            for k, v in flt.items():
                if not f.mock.has_field(k):
                    RuntimeError("User doesn't have field '{}'.".format(k))

                if isinstance(v, (tuple, list)):
                    f.inc(k, v)
                else:
                    f.eq(k, v)

        return f.count()

    def count_roles(self, flt: dict = None) -> int:
        f = _odm.find('role')
        if flt:
            for k, v in flt.items():
                if not f.mock.has_field(k):
                    RuntimeError("Role doesn't have field '{}'.".format(k))

                f.eq(k, v)

        return f.count()

    def get_user_modify_form(self, user: _auth.model.AbstractUser = None) -> _form.Form:
        return _odm_ui.get_m_form('user', user.uid) if user else _odm_ui.get_m_form('user')
