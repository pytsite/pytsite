from ..core import odm


class User(odm.Model):
    def _setup(self):
        self.define_field(odm.StringField('login', not_empty=True))
        self.define_field(odm.StringField('email', not_empty=True))
        self.define_field(odm.StringField('password', not_empty=True))
        self.define_field(odm.StringField('fullName', not_empty=True))
        self.define_field(odm.DateTimeField('lastLogin'))


