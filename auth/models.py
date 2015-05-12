from ..core import odm


class User(odm.models.Model):
    def _setup(self):
        self.define_field(odm.fields.StringField('login', not_empty=True))
        self.define_field(odm.fields.StringField('email', not_empty=True))
        self.define_field(odm.fields.StringField('password', not_empty=True))
        self.define_field(odm.fields.StringField('fullName'))
        self.define_field(odm.fields.DateTimeField('lastLogin'))
        self.define_field(odm.fields.IntegerField('loginCount'))
        self.define_field(odm.fields.StringField('status'))
        self.define_field(odm.fields.StringField('token'))
        self.define_field(odm.fields.StringField('groups'))
        self.define_field(odm.fields.IntegerField('gender'))
        self.define_field(odm.fields.StringField('phone'))
        self.define_field(odm.fields.DictField('options'))
        self.define_field(odm.fields.RefField('picture'))

        self.define_index([('login', odm.I_ASC)], unique=True)
