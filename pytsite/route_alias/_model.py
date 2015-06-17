"""Route Alias Model.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core import odm


class RouteAliasModel(odm.model.ODMModel):
    """Taxonomy Term Model.
    """
    def _setup(self):
        """Hook.
        """
        self._define_field(odm.field.String('alias', not_empty=True))
        self._define_field(odm.field.String('target'))
        self._define_field(odm.field.String('language', not_empty=True))

        self._define_index([('alias', odm.I_ASC), ('language', odm.I_ASC)], unique=True)

    def _on_f_set(self, field_name: str, value, **kwargs):
        """Hook.
        """
        if field_name == 'alias':
            from . import _manager
            value = _manager.sanitize_alias_string(value)

        return super()._on_f_set(field_name, value, **kwargs)
