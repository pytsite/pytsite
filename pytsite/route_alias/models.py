"""Route Alias Model.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


from pytsite.core.odm.models import ODMModel
from pytsite.core.odm import I_ASC
from pytsite.core.odm.fields import *


class RouteAliasModel(ODMModel):
    """Taxonomy Term Model.
    """

    def _setup(self):
        """Hook.
        """
        self._define_field(StringField('alias', not_empty=True))
        self._define_field(StringField('target'))
        self._define_field(StringField('language', not_empty=True))

        self._define_index([('alias', I_ASC), ('language', I_ASC)], unique=True)

    def _on_f_set(self, field_name: str, value, **kwargs):
        """Hook.
        """
        if field_name == 'alias':
            from . import route_alias_manager
            value = route_alias_manager.sanitize_alias_string(value)

        return super()._on_f_set(field_name, value, **kwargs)
