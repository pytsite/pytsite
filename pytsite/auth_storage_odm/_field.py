"""PytSite Auth Storage ODM Fields.
"""
from bson import DBRef as _DBRef
from typing import Tuple as _Tuple, List as _List, Iterable as _Iterable, Optional as _Optional, Union as _Union
from pytsite import odm as _odm, auth as _auth

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Roles(_odm.field.UniqueStringList):
    def _get_role_uid(self, value) -> str:
        """Helper
        """
        if isinstance(value, _auth.model.AbstractRole):
            return value.uid
        elif isinstance(value, str):
            return _auth.get_role(uid=value).uid
        elif isinstance(value, _DBRef):
            return _auth.get_role(uid=str(value.id)).uid
        else:
            raise TypeError("Field '{}': role object, str or DB ref expected, got {}".format(self.name, type(value)))

    def _on_get(self, value: _List[str], **kwargs) -> _Tuple[_auth.model.AbstractRole, ...]:
        return tuple([_auth.get_role(uid=role_uid) for role_uid in value])

    def _on_set(self, value: _Iterable, **kwargs) -> _List[str]:
        """Hook
        """
        if value is None:
            return []

        if not isinstance(value, (list, tuple)):
            raise TypeError("Field '{}': list or tuple expected, got {}".format(self.name, type(value)))

        return [self._get_role_uid(r) for r in value]

    def _on_add(self, current_value: list, raw_value_to_add, **kwargs):
        return super()._on_add(current_value, self._get_role_uid(raw_value_to_add))

    def _on_sub(self, current_value: list, raw_value_to_sub, **kwargs):
        return super()._on_sub(current_value, self._get_role_uid(raw_value_to_sub))

    def sanitize_finder_arg(self, arg):
        """Hook. Used for sanitizing Finder's query argument.
        """
        if isinstance(arg, _auth.model.AbstractRole):
            return arg.uid
        elif isinstance(arg, (list, tuple)):
            clean_arg = []
            for role in arg:
                if isinstance(role, _auth.model.AbstractRole):
                    clean_arg.append(role.uid)
                else:
                    clean_arg.append(role)
            return clean_arg
        else:
            return arg


class User(_odm.field.Abstract):
    """Field to store reference to user
    """

    def __init__(self, name: str, **kwargs):
        """Init.

        :param default:
        :param nonempty: bool
        :param allow_anonymous: bool
        :param allow_system: bool
        """
        self._allow_anonymous = kwargs.get('allow_anonymous', False)
        self._allow_system = kwargs.get('allow_system', False)
        self._disallowed_users = kwargs.get('disallowed_users', ())

        super().__init__(name, **kwargs)

    def _resolve_user(self, value) -> _auth.model.AbstractUser:
        if isinstance(value, _auth.model.AbstractUser):
            return value
        elif isinstance(value, str):
            return _auth.get_user(uid=value)
        elif isinstance(value, _DBRef):
            return _auth.get_user(uid=value.id)
        else:
            raise TypeError("Field '{}': user object, str or DB ref expected, got {}.".
                            format(self._name, type(value)))

    def _check_user(self, user: _auth.model.AbstractUser):
        if user.is_anonymous:
            if not self._allow_anonymous:
                raise ValueError('Anonymous user is not allowed here')
            return 'ANONYMOUS'
        elif user.is_system:
            if not self._allow_system:
                raise ValueError('System user is not allowed here')
            return 'SYSTEM'

        if self._disallowed_users:
            for user in self._disallowed_users:  # type: _auth.model.AbstractUser
                if user.uid == user.uid:
                    raise ValueError("User '{}' is not allowed here".format(user.login))

        return user

    def _on_set(self, value, **kwargs) -> str:
        """Hook

        Internally this field stores only user's UID as string.
        """
        value = self._check_user(self._resolve_user(value))

        if value.is_anonymous:
            return 'ANONYMOUS'
        elif value.is_system:
            return 'SYSTEM'

        return value.uid

    def _on_get(self, value: str, **kwargs) -> _Optional[_auth.model.AbstractUser]:
        """Hook
        """
        if value == 'ANONYMOUS':
            return _auth.get_anonymous_user()
        elif value == 'SYSTEM':
            return _auth.get_system_user()
        else:
            return _auth.get_user(uid=value) if value else None

    def sanitize_finder_arg(self, arg):
        """Hook. Used for sanitizing Finder's query argument.
        """
        if isinstance(arg, _auth.model.AbstractUser):
            if arg.is_anonymous:
                return 'ANONYMOUS'
            elif arg.is_system:
                return 'SYSTEM'
            else:
                return arg.uid
        elif isinstance(arg, (list, tuple)):
            clean_arg = []
            for user in arg:
                if isinstance(user, _auth.model.AbstractUser):
                    clean_arg.append(user.uid)
                else:
                    clean_arg.append(user)
            return clean_arg
        else:
            return arg


class Users(User):
    """Field to store list of references to users
    """

    def __init__(self, name: str, **kwargs):
        """Init.
        """
        kwargs.setdefault('default', [])

        super().__init__(name, **kwargs)

    def _on_set(self, value: _Union[list, tuple], **kwargs) -> _List[str]:
        """Hook
        """
        if not isinstance(value, (list, tuple)):
            raise TypeError("Field '{}': list or tuple expected, got {}".format(self.name, type(value)))

        return [self._check_user(self._resolve_user(v)).uid for v in value]

    def _on_get(self, value: list, **kwargs) -> _Tuple[_auth.model.AbstractUser, ...]:
        """Hook
        """
        r = []
        for uid in value:
            try:
                r.append(_auth.get_user(uid=uid))
            except _auth.error.UserNotExist:
                pass

        return tuple(r)

    def _on_add(self, current_value: list, raw_value_to_add, **kwargs):
        current_value.append(self._check_user(self._resolve_user(raw_value_to_add)).uid)

        return current_value

    def _on_sub(self, current_value: list, raw_value_to_sub, **kwargs):
        raw_value_to_sub = self._check_user(self._resolve_user(raw_value_to_sub)).uid

        return [uid for uid in current_value if uid != raw_value_to_sub]
