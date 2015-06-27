"""Flag Package Models.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core import odm as _odm

class Flag(_odm.Model):
    """Flag ODM Model.
    """
    def _setup(self):
        """Hook.
        """
        self._define_field(_odm.field.String('uid', not_empty=True))
        self._define_field(_odm.field.Ref('author', model='user', not_empty=True))

        self._define_index([('uid', _odm.I_ASC), ('author', _odm.I_ASC)])
