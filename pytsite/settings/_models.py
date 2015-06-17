"""Settings Models.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


from pytsite.core.odm import I_ASC
from pytsite.core.odm._model import ODMModel
from pytsite.core.odm._field import String, Dict


class SettingModel(ODMModel):
    def _setup(self):
        """Hook.
        """
        self._define_field(String('uid', not_empty=True))
        self._define_field(Dict('value'))

        self._define_index([('uid', I_ASC)])