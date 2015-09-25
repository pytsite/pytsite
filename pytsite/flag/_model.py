"""Flag Package Models.
"""
from pytsite import odm as _odm

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Flag(_odm.Model):
    """Flag ODM Model.
    """
    def _setup(self):
        """Hook.
        """
        self._define_field(_odm.field.Ref('entity', model='*', nonempty=True))
        self._define_field(_odm.field.Ref('author', model='user', nonempty=True))

        self._define_index([('entity', _odm.I_ASC), ('author', _odm.I_ASC)], unique=True)
