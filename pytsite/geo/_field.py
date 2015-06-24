"""Description.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core import odm as _odm


class GeoLocationField(_odm.field.Dict):
    """Geo Location Field.
    """
    def set_val(self, value: dict, change_modified: bool=True, **kwargs):
        if isinstance(value, dict) and value:
            if 'address' not in value or not value['address']:
                raise ValueError('Address is not defined.')
            if 'components' not in value or not isinstance(value['components'], list) or not value['components']:
                raise ValueError('Components is not defined.')
            if 'lng_lat' not in value or not isinstance(value['lng_lat'], list) or not value['lng_lat']:
                raise ValueError('Geometry is not defined.')
            if not isinstance(value['lng_lat'][0], float) or not isinstance(value['lng_lat'][1], float):
                raise ValueError('Invalid format of geometry.')

        return super().set_val(value, change_modified, **kwargs)
