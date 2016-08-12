"""Flag Package Models.
"""
from pytsite import odm as _odm, odm_auth as _odm_auth

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Flag(_odm_auth.model.AuthorizableEntity):
    """Flag ODM Model.
    """
    def _setup_fields(self):
        """Hook.
        """
        self.define_field(_odm.field.String('type', default='default'))
        self.define_field(_odm.field.Ref('entity', nonempty=True))
        self.define_field(_odm.field.Ref('author', model='user', nonempty=True))
        self.define_field(_odm.field.Decimal('score', default=1))

    def _setup_indexes(self):
        """Hook.
        """
        self.define_index([('entity', _odm.I_ASC), ('author', _odm.I_ASC)], unique=True)
