"""PytSIte Authentication ODM Storage Driver.
"""
from typing import Iterable as _Iterable, Union as _Union
from pytsite import auth as _auth, odm as _odm, form as _form, odm_ui as _odm_ui
from . import _model

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Driver(_auth.driver.Storage):
    def get_name(self) -> str:
        return 'odm'

    def create_role(self, name: str, description: str = '') -> _auth.model.AbstractRole:
        role = _odm.dispense('role')  # type: _model.Role
        role.name = name
        role.description = description
        role.save()

        return role

    def get_role(self, name: str = None, uid: str = None) -> _auth.model.AbstractRole:
        f = _odm.find('role')

        if name:
            f.where('name', '=', name)
        elif uid:
            f.where('_id', '=', uid)
        else:
            raise RuntimeError("Either role's name or UID should be specified.")

        role = f.first()
        if not role:
            raise _auth.error.RoleNotExist("Role '{}' does not exist.".format(name))

        return role

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

                f.where(k, '=', v)

        return f.get(limit)

    def create_user(self, login: str, password: str = None) -> _auth.model.AbstractUser:
        user = _odm.dispense('user')  # type: _model.User
        user.login = login
        user.email = login
        user.password = password

        if not user.is_anonymous and not user.is_system:
            user.save()

        return user

    def get_user(self, login: str = None, nickname: str = None, access_token: str = None,
                 uid: str = None) -> _auth.model.AbstractUser:
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
                    f.where(k, 'in', v)
                else:
                    f.where(k, '=', v)

        return f.get(limit)

    def count_users(self, flt: dict = None) -> int:
        f = _odm.find('user')
        if flt:
            for k, v in flt.items():
                if not f.mock.has_field(k):
                    RuntimeError("User doesn't have field '{}'.".format(k))

                if isinstance(v, (tuple, list)):
                    f.where(k, 'in', v)
                else:
                    f.where(k, '=', v)

        return f.count()

    def count_roles(self, flt: dict = None) -> int:
        f = _odm.find('role')
        if flt:
            for k, v in flt.items():
                if not f.mock.has_field(k):
                    RuntimeError("Role doesn't have field '{}'.".format(k))

                f.where(k, '=', v)

        return f.count()

    def update_entity(self, entity: _Union[_auth.model.AuthEntity, _model.User, _model.Role]):
        entity.save()

    def delete_entity(self, entity: _Union[_auth.model.AuthEntity, _model.User, _model.Role]):
        entity.delete()

    def get_user_modfy_form(self, user: _auth.model.AbstractUser = None) -> _form.Form:
        return _odm_ui.get_m_form('user', user.uid) if user else _odm_ui.get_m_form('user')

    def get_role_modify_form(self, role: _auth.model.AbstractRole = None) -> _form.Form:
        return _odm_ui.get_m_form('role', role.uid) if role else _odm_ui.get_m_form('role')
