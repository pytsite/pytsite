""" Auth Models.
"""

import hashlib
from pytsite.core import util
from pytsite.core.odm import I_ASC
from pytsite.core.odm.model import ODMModel
from pytsite.core.odm.fields import *
from pytsite.odm_ui.models import ODMUIModel


class User(ODMModel, ODMUIModel):
    """User.
    """

    def _setup(self):
        """_setup() hook.
        """

        self.define_field(StringField('login', required=True))
        self.define_field(StringField('email', required=True, validate_email=True))
        self.define_field(StringField('password', required=True))
        self.define_field(StringField('token', required=True))
        self.define_field(StringField('fullName'))
        self.define_field(DateTimeField('lastLogin'))
        self.define_field(IntegerField('loginCount'))
        self.define_field(StringField('status', default='active'))
        self.define_field(RefsListField('roles', model='role'))
        self.define_field(IntegerField('gender'))
        self.define_field(StringField('phone'))
        self.define_field(DictField('options'))
        self.define_field(RefField('picture'))

        self.define_index([('login', I_ASC)], unique=True)
        self.define_index([('token', I_ASC)], unique=True)

    def _on_f_set(self, field_name: str, orig_value, **kwargs):
        """_on_f_set() hook.
        """
        if field_name == 'password':
            from .auth_manager import password_hash
            orig_value = password_hash(orig_value)
            self.f_set('token', hashlib.md5(util.random_password().encode()).hexdigest())

        return orig_value

    def _pre_save(self):
        """_pre_save() hook.
        """

        if self.f_get('login') == '__anonymous':
            raise Exception('Anonymous user cannot be saved.')

        if not self.f_get('password'):
            self.f_set('password', util.random_password())

    def has_role(self, name: str) -> bool:
        """Checks if the user has role.
        """

        for role in self.f_get('roles'):
            if role.f_get('name') == name:
                return True

        return False

    def has_permission(self, name: str) -> bool:
        """Checks if the user has permission.
        """

        from . import auth_manager
        if not auth_manager.is_permission_defined(name):
            raise KeyError("Permission '{}' is not defined.".format(name))

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

    def is_admin(self):
        """Check if the user is admin.
        """

        return self.has_role('admin')


class Role(ODMModel):
    """Role.
    """

    def _setup(self):
        """_setup() hook.
        """

        self.define_field(StringField('name', required=True))
        self.define_field(StringField('description'))
        self.define_field(ListField('permissions'))

        self.define_index([('name', I_ASC)], unique=True)

    def _on_f_add(self, field_name: str, value, **kwargs: dict):
        """_on_f_add() hook.
        """

        if field_name == 'permissions' and not isinstance(value, str):
            raise TypeError("String expected")

        return value
