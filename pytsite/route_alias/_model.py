"""Route Alias Model.
"""
from pytsite import odm as _odm

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class RouteAlias(_odm.Model):
    """Taxonomy Term Model.
    """
    def _setup(self):
        """Hook.
        """
        self._define_field(_odm.field.String('alias', nonempty=True))
        self._define_field(_odm.field.String('target', nonempty=True))
        self._define_field(_odm.field.String('language', nonempty=True))

        self._define_index([('alias', _odm.I_ASC), ('language', _odm.I_ASC)], unique=True)

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
