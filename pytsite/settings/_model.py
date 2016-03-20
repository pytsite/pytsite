"""Settings Models.
"""
from pytsite import odm as _odm

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Setting(_odm.Entity):
    def _setup_fields(self):
        """Hook.
        """
        self.define_field(_odm.field.String('uid', nonempty=True))
        self.define_field(_odm.field.Dict('value'))

    def _setup_indexes(self):
        """Hook.
        """
        self.define_index([('uid', _odm.I_ASC)])
