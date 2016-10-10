"""PytSite Auth Storage ODM Fields.
"""
from bson import DBRef as _DBRef
from typing import List as _List, Iterable as _Iterable
from pytsite import odm as _odm, auth as _auth


__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Roles(_odm.field.UniqueStringList):
    def __init__(self, name: str, **kwargs):
        """Init.

        :param default:
        :param nonempty: bool
        """
        self._roles = []
        super().__init__(name, **kwargs)

    def _get_role(self, value) -> _auth.model.AbstractRole:
        if isinstance(value, _auth.model.AbstractRole):
            return value
        elif isinstance(value, str):
            return _auth.get_role(uid=value)
        elif isinstance(value, _DBRef):
            return _auth.get_role(uid=str(value.id))
        else:
            raise TypeError("Field '{}': role object, str or DB ref expected, got {}.".format(self.name, type(value)))

    def _on_set(self, value: _Iterable, **kwargs) -> _List[str]:
        """Hook. Transforms externally set value to internal value.
        """
        if not isinstance(value, (list, tuple)):
            raise TypeError("Field '{}': list or tuple expected, got {}.".format(self.name, type(value)))

        self._roles = []
        clean_value = []
        for r in value:
            role = self._get_role(r)
            clean_value.append(role.uid)
            self._roles.append(role)

        return clean_value

    def _on_get(self, internal_value: str, **kwargs) -> _auth.model.AbstractUser:
        """Hook. Transforms internal value to external one.
        """
        return self._roles

    def _on_add(self, internal_value, value_to_add, **kwargs):
        return super()._on_add(internal_value, self._get_role(value_to_add).uid)

    def _on_sub(self, internal_value, value_to_sub, **kwargs):
        return super()._on_sub(internal_value, self._get_role(value_to_sub).uid)
    
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
    """Field to store reference to user.
    """

    def __init__(self, name: str, **kwargs):
        """Init.

        :param default:
        :param nonempty: bool
        """
        self._user = None
        super().__init__(name, **kwargs)

    def _convert_value_to_user(self, value) -> _auth.model.AbstractUser:
        if isinstance(value, _auth.model.AbstractUser):
            return value
        elif isinstance(value, str):
            return _auth.get_user(uid=value, check_status=False)
        elif isinstance(value, _DBRef):
            return _auth.get_user(uid=str(value.id), check_status=False)
        else:
            raise TypeError("Field '{}': user object, str or DB ref expected, got {}.".
                            format(self._name, type(value)))

    def _on_set(self, value, **kwargs) -> str:
        """Hook. Transforms externally set value to internal value.
        """
        # Cache user object for self._on_get()
        try:
            self._user = self._convert_value_to_user(value)
        except _auth.error.UserNotExist:
            self._user = _auth.get_first_admin_user()

        # Internally this field stores only user's UID as string
        return self._user.uid

    def _on_get(self, internal_value: str, **kwargs) -> _auth.model.AbstractUser:
        """Hook. Transforms internal value to external one.
        """
        return self._user

    def sanitize_finder_arg(self, arg):
        """Hook. Used for sanitizing Finder's query argument.
        """
        if isinstance(arg, _auth.model.AbstractUser):
            return arg.uid
        elif isinstance(arg, (list, tuple)):
            clean_arg = []
            for role in arg:
                if isinstance(role, _auth.model.AbstractUser):
                    clean_arg.append(role.uid)
                else:
                    clean_arg.append(role)
            return clean_arg
        else:
            return arg
