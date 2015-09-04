"""Geo ODM Fields.
"""
from pytsite import odm as _odm

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class LngLat(_odm.field.FloatList):
    """Geo longitude and latitude field.
    """
    def __init__(self, name: str, **kwargs):
        """Init.
        """
        super().__init__(name, default=[0.0, 0.0], min_len=2, max_len=2, **kwargs)

    def __bool__(self):
        """Checks if the field is empty.
        """
        return self._value != [0.0, 0.0]


class Location(_odm.field.Abstract):
    """Geo Location Field.
    """
    def set_val(self, value, change_modified: bool=True, **kwargs):
        """Hook.
        :param value: dict | list | tuple
        """
        if isinstance(value, dict):
            # Checking all necessary keys
            for k in ('lng', 'lat', 'accuracy', 'alt', 'alt_accuracy', 'heading', 'speed'):
                if k in value:
                    try:
                        value[k] = float(value[k])
                    except ValueError:
                        value[k] = 0.0
                else:
                    value[k] = 0.0

            # Settings 'lat_lng' value
            value['lng_lat'] = [value['lng'], value['lat']]

            # Checking address
            if 'address' in value:
                if not isinstance(value['address'], str):
                    raise ValueError("'address' must be string.")
            else:
                value['address'] = ''

            # Checking address components
            if 'address_components' in value:
                if not isinstance(value['address_components'], list):
                    raise ValueError("'address_components' must be list.")
            else:
                value['address_components'] = []

        elif type(value) in (tuple, list):
            if len(value) == 2:
                value = {
                    'lng': value[0],
                    'lat': value[1],
                    'lng_lat': [value[0], value[1]],
                    'accuracy': 0.0,
                    'alt': 0.0,
                    'alt_accuracy': 0.0,
                    'heading': 0.0,
                    'speed': 0.0,
                    'address': '',
                    'address_components': [],
                }

        elif value is not None:
            raise ValueError("Field '{}': dict, list or tuple expected.".format(self.name))

        return super().set_val(value, change_modified, **kwargs)
