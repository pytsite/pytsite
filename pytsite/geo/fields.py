"""Description.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core.odm.fields import DictField


class GeoLocationField(DictField):
    """Geo Location Field.
    """

    def set_val(self, value: dict, change_modified: bool=True, **kwargs):
        if isinstance(value, dict):
            if 'address' not in value or not value['address']:
                raise ValueError('Address is not defined.')
            if 'components' not in value or not isinstance(value['components'], list) or not value['components']:
                raise ValueError('Components is not defined.')
            if 'geometry' not in value or not isinstance(value['geometry'], list) or not value['geometry']:
                raise ValueError('Geometry is not defined.')
            if 'lng' not in value['geometry'] or 'lat' not in value['geometry']:
                raise ValueError('Invalid format of geometry.')
            if not isinstance(value['geometry']['lng'], float) or not isinstance(value['geometry']['lat'], float):
                raise ValueError('Invalid format of geometry.')

        return super().set_val(value, change_modified, **kwargs)
