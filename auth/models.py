""" Auth Models.
"""

import hashlib
from pytsite.core import odm, util


class User(odm.models.Model):
    """User.
    """

    def _setup(self):
        """_setup() hook.
        """

        self.define_field(odm.fields.StringField('login', required=True))
        self.define_field(odm.fields.StringField('email', required=True, validate_email=True))
        self.define_field(odm.fields.StringField('password', required=True))
        self.define_field(odm.fields.StringField('token', required=True))
        self.define_field(odm.fields.StringField('fullName'))
        self.define_field(odm.fields.DateTimeField('lastLogin'))
        self.define_field(odm.fields.IntegerField('loginCount'))
        self.define_field(odm.fields.StringField('status', default='active'))
        self.define_field(odm.fields.RefsListField('roles', model='role'))
        self.define_field(odm.fields.IntegerField('gender'))
        self.define_field(odm.fields.StringField('phone'))
        self.define_field(odm.fields.DictField('options'))
        self.define_field(odm.fields.RefField('picture'))

        self.define_index([('login', odm.I_ASC)], unique=True)
        self.define_index([('token', odm.I_ASC)], unique=True)

    def _on_f_set(self, field_name: str, orig_value, **kwargs):
        """_on_f_set() hook.
        """
        if field_name == 'password':
            from .manager import password_hash
            orig_value = password_hash(orig_value)
            self.f_set('token', hashlib.md5(util.random_password().encode()).hexdigest())

        return orig_value

    def _pre_save(self):
        """_pre_save() hook.
        """
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

        from . import manager
        if not manager.is_permission_defined(name):
            raise KeyError("Permission '{}' is not defined.".format(name))

        if self.has_role('admin'):
            return True

        for role in self.f_get('roles'):
            if name in role.f_get('permissions'):
                return True

        return False


class Role(odm.models.Model):
    """Role.
    """

    def _setup(self):
        """_setup() hook.
        """

        self.define_field(odm.fields.StringField('name', required=True))
        self.define_field(odm.fields.StringField('description'))
        self.define_field(odm.fields.ListField('permissions'))

        self.define_index([('name', odm.I_ASC)], unique=True)

    def _on_f_add(self, field_name: str, value, **kwargs: dict):
        """_on_f_add() hook.
        """

        if field_name == 'permissions' and not isinstance(value, str):
            raise TypeError("String expected")

        return value
