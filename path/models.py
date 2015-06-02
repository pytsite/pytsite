"""Path Model.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


from pytsite.core.odm.models import ODMModel
from pytsite.core.odm import I_ASC
from pytsite.core.odm.fields import *


class Path(ODMModel):
    """Taxonomy Term Model.
    """

    def _setup(self):
        self._define_field(StringField('alias', not_empty=True))
        self._define_field(StringField('target', not_empty=True))
        self._define_field(StringField('language', not_empty=True))
        self._define_index([('alias', I_ASC), ('language', I_ASC)], unique=True)
