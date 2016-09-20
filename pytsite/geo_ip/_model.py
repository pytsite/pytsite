"""GeoIP Package ODM Models.
"""
from pytsite import odm as _odm, geo as _geo

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class GeoIP(_odm.model.Entity):
    @property
    def ip(self) -> str:
        return self.f_get('ip')

    @property
    def asn(self) -> str:
        return self.f_get('asn')

    @property
    def city(self) -> str:
        return self.f_get('city')

    @property
    def country(self) -> str:
        return self.f_get('country')

    @property
    def country_code(self) -> str:
        return self.f_get('country_code')

    @property
    def isp(self) -> str:
        return self.f_get('isp')

    @property
    def location(self) -> dict:
        return self.f_get('location')

    def organization(self) -> str:
        return self.f_get('organization')

    @property
    def postal_code(self) -> int:
        return self.f_get('postal_code')

    @property
    def region(self) -> str:
        return self.f_get('region')

    @property
    def region_name(self) -> str:
        return self.f_get('region_name')

    @property
    def timezone(self) -> str:
        return self.f_get('timezone')

    def _setup_fields(self):
        """Hook.
        """
        self.define_field(_odm.field.String('ip', required=True))
        self.define_field(_odm.field.String('asn'))
        self.define_field(_odm.field.String('city'))
        self.define_field(_odm.field.String('country'))
        self.define_field(_odm.field.String('country_code'))
        self.define_field(_odm.field.String('isp'))
        self.define_field(_odm.field.Virtual('longitude'))
        self.define_field(_odm.field.Virtual('latitude'))
        self.define_field(_geo.field.Location('location'))
        self.define_field(_odm.field.String('organization'))
        self.define_field(_odm.field.String('postal_code'))
        self.define_field(_odm.field.String('region'))
        self.define_field(_odm.field.String('region_name'))
        self.define_field(_odm.field.String('timezone'))

    def _setup_indexes(self):
        """Hook.
        """
        self.define_index([('ip', _odm.I_ASC)], unique=True)
        self.define_index([('location.geo_point', _odm.I_GEOSPHERE)])

    def _on_f_set(self, field_name: str, value, **kwargs):
        """Hook.
        """
        if field_name == 'longitude':
            self.f_set('location', {'lng': value, 'lat': self.location['lat']})
        elif field_name == 'latitude':
            self.f_set('location', {'lng': self.location['lng'], 'lat': value})

        return super()._on_f_set(field_name, value, **kwargs)
