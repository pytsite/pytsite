"""Settings Models.
"""
from pytsite import odm as _odm

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Setting(_odm.Model):
    def _setup(self):
        """Hook.
        """
        self._define_field(_odm.field.String('uid', nonempty=True))
        self._define_field(_odm.field.Dict('value'))

        self._define_index([('uid', _odm.I_ASC)])
