"""PytSite Language UI ODM Models
"""
from pytsite import odm as _odm, lang as _lang

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Translation(_odm.model.Entity):
    def _setup_fields(self):
        self.define_field(_odm.field.String('message_id', required=True))
        self.define_field(_odm.field.String('translation', required=True))
        self.define_field(_odm.field.String('language', required=True, default=_lang.get_current()))

    def _setup_indexes(self):
        self.define_index([('message_id', _odm.I_ASC), ('language', _odm.I_ASC)], True)
