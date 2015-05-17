import hashlib
from pytsite.core import odm, util


class User(odm.models.Model):
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
        self.define_field(odm.fields.ListField('groups'))
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


class Group(odm.models.Model):
    def _setup(self):
        """_setup() hook.
        """

        self.define_field(odm.fields.StringField('name', required=True))
        self.define_field(odm.fields.StringField('description'))
        self.define_field(odm.fields.ListField('permissions'))

        self.define_index([('name', odm.I_ASC)], unique=True)
