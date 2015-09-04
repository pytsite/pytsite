"""GeoIP Package ODM Models.
"""
from pytsite import odm as _odm, geo as _geo

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class GeoIP(_odm.Model):
    @property
    def ip(self) -> str:
        return self.f_get('ip')

    @property
    def longitude(self) -> float:
        return self.f_get('longitude')

    @property
    def latitude(self) -> float:
        return self.f_get('latitude')

    @property
    def lng_lat(self) -> list:
        return self.f_get('lng_lat')

    @property
    def area_code(self) -> int:
        return self.f_get('area_code')

    @property
    def dma_code(self) -> int:
        return self.f_get('dma_code')

    @property
    def postal_code(self) -> int:
        return self.f_get('postal_code')

    @property
    def continent_code(self) -> str:
        return self.f_get('continent_code')

    @property
    def country_code(self) -> str:
        return self.f_get('country_code')

    @property
    def country_code3(self) -> str:
        return self.f_get('country_code3')

    @property
    def country(self) -> str:
        return self.f_get('country')

    @property
    def region_code(self) -> str:
        return self.f_get('region_code')

    @property
    def region(self) -> str:
        return self.f_get('region')

    @property
    def city(self) -> str:
        return self.f_get('city')

    @property
    def timezone(self) -> str:
        return self.f_get('timezone')

    @property
    def isp(self) -> str:
        return self.f_get('isp')

    @property
    def asn(self) -> str:
        return self.f_get('asn')

    def _setup(self):
        """Hook.
        """
        self._define_field(_odm.field.String('ip'))
        self._define_field(_odm.field.Float('longitude'))
        self._define_field(_odm.field.Float('latitude'))
        self._define_field(_geo.odm_field.LngLat('lng_lat'))
        self._define_field(_odm.field.Integer('area_code'))
        self._define_field(_odm.field.Integer('dma_code'))
        self._define_field(_odm.field.Integer('postal_code'))
        self._define_field(_odm.field.String('continent_code'))
        self._define_field(_odm.field.String('country_code'))
        self._define_field(_odm.field.String('country_code3'))
        self._define_field(_odm.field.String('country'))
        self._define_field(_odm.field.String('region_code'))
        self._define_field(_odm.field.String('region'))
        self._define_field(_odm.field.String('city'))
        self._define_field(_odm.field.String('timezone'))
        self._define_field(_odm.field.String('isp'))
        self._define_field(_odm.field.String('asn'))

        self._define_index(('ip', _odm.I_ASC), unique=True)
        self._define_index(('lng_lat', _odm.I_GEO2D))

    def _on_f_set(self, field_name: str, value, **kwargs):
        """Hook.
        """
        if field_name == 'longitude':
            self.f_set('lng_lat', [value, self.latitude])

        if field_name == 'latitude':
            self.f_set('lng_lat', [self.longitude, value])

        return value
