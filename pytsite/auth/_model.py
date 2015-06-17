""" Auth Models.
"""

import hashlib
from pytsite.core import util
from pytsite.core.odm import I_ASC
from pytsite.core.odm._model import ODMModel
from pytsite.core.odm._field import *


class User(ODMModel):
    """User Model.
    """

    def _setup(self):
        """_setup() hook.
        """

        # Fields
        self._define_field(String('login'))
        self._define_field(String('email'))
        self._define_field(String('password'))
        self._define_field(String('token'))
        self._define_field(String('first_name'))
        self._define_field(String('last_name'))
        self._define_field(String('full_name'))
        self._define_field(DateTime('birth_date'))
        self._define_field(DateTime('last_login'))
        self._define_field(Integer('login_count'))
        self._define_field(String('status', default='active'))
        self._define_field(RefsListField('roles', model='role'))
        self._define_field(Bool('profile_is_public'))
        self._define_field(Integer('gender'))
        self._define_field(String('phone'))
        self._define_field(Dict('options'))
        self._define_field(Ref('picture', model='image'))

        # Indices
        self._define_index([('login', I_ASC)], unique=True)
        self._define_index([('token', I_ASC)], unique=True)

    def _on_f_set(self, field_name: str, value, **kwargs):
        """_on_f_set() hook.
        """
        if field_name == 'password':
            from ._manager import password_hash
            value = password_hash(value)
            self.f_set('token', hashlib.md5(util.random_password().encode()).hexdigest())

        return value

    def _pre_save(self):
        """_pre_save() hook.
        """
        if self.f_get('login') == '__anonymous':
            raise Exception('Anonymous user cannot be saved.')

        if not self.f_get('password'):
            self.f_set('password', util.random_password())

    def has_role(self, name: str) -> bool:
        """Checks if the user has a role.
        """
        for role in self.f_get('roles'):
            if role.f_get('name') == name:
                return True

        return False

    def has_permission(self, name: str) -> bool:
        """Checks if the user has permission.
        """
        from . import _manager
        if not _manager.is_permission_defined(name):
            raise KeyError("Permission '{}' is not defined.".format(name))

        # Admin 'has' any role
        if self.is_admin():
            return True

        for role in self.f_get('roles'):
            if name in role.f_get('permissions'):
                return True

        return False

    def is_anonymous(self) -> bool:
        """Check if the user is anonymous.
        """
        return self.f_get('login') == '__anonymous'

    def is_admin(self) -> bool:
        """Check if the user has the 'admin' role.
        """
        return self.has_role('admin')


class Role(ODMModel):
    """Role.
    """

    def _setup(self):
        """_setup() hook.
        """

        self._define_field(String('name'))
        self._define_field(String('description'))
        self._define_field(UniqueListField('permissions'))

        self._define_index([('name', I_ASC)], unique=True)

    def _on_f_add(self, field_name: str, value, **kwargs: dict):
        """_on_f_add() hook.
        """

        if field_name == 'permissions' and not isinstance(value, str):
            raise TypeError("String expected")

        return value
