"""Route Alias Model.
"""
from pytsite import odm as _odm, router as _router

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class RouteAlias(_odm.Entity):
    """Taxonomy Term Model.
    """
    def _setup_fields(self):
        """Hook.
        """
        self.define_field(_odm.field.String('alias', nonempty=True))
        self.define_field(_odm.field.String('target', nonempty=True))
        self.define_field(_odm.field.String('language', nonempty=True))

    def _setup_indexes(self):
        """Hook.
        """
        self.define_index([('alias', _odm.I_ASC), ('language', _odm.I_ASC)], unique=True)

    @property
    def alias(self) -> str:
        return self.f_get('alias')

    @property
    def target(self) -> str:
        return self.f_get('target')

    @property
    def language(self) -> str:
        return self.f_get('language')

    def _on_f_set(self, field_name: str, value, **kwargs):
        """Hook.
        """
        if field_name == 'alias':
            from . import _api
            value = _api.sanitize_alias_string(value, self.language)

        return super()._on_f_set(field_name, value, **kwargs)

    def _after_delete(self):
        """Hook.
        """
        _router.remove_path_alias(self.alias)
