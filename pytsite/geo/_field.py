"""Geo ODM Fields
"""
from typing import Union as _Union
from frozendict import frozendict as _frozendict
from pytsite import odm as _odm

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Location(_odm.field.Dict):
    """Geo Location Field.
    """
    def __init__(self, name: str, **kwargs):
        default = kwargs.get('default', {
            'lng': 0.0,
            'lat': 0.0,
            'accuracy': 0.0,
            'alt': 0.0,
            'alt_accuracy': 0.0,
            'heading': 0.0,
            'speed': 0.0,
        })

        # Helper for building MongoDB's indexes
        default['geo_point'] = {
            'type': 'Point',
            'coordinates': (default['lng'], default['lat'])
        }

        super().__init__(name, default=default, keys=('lng', 'lat'), **kwargs)

    @property
    def is_empty(self) -> bool:
        return self.get_val()['coordinates'] == (0.0, 0.0)

    def set_val(self, value: _Union[dict, _frozendict], **kwargs):
        """Hook.
        """
        if isinstance(value, _frozendict):
            value = dict(value)

        if isinstance(value, (dict, _frozendict)):
            # Checking and setting up all necessary keys
            for k in ('lng', 'lat', 'accuracy', 'alt', 'alt_accuracy', 'heading', 'speed'):
                if k in value:
                    try:
                        value[k] = float(value[k])
                    except ValueError:
                        value[k] = 0.0
                else:
                    value[k] = 0.0

            value['geo_point'] = {
                'type': 'Point',
                'coordinates': (value['lng'], value['lat']),
            }

        elif value is not None:
            raise ValueError("Field '{}': dict or None expected.".format(self.name))

        return super().set_val(value, **kwargs)


class Address(_odm.field.Dict):
    """Geo Address Field.
    """
    def __init__(self, name: str, **kwargs):
        """Init.
        """
        default = kwargs.get('default', {
            'lng': 0.0,
            'lat': 0.0,
            'address': '',
            'address_components': [],
        })

        # Helper for building MongoDB's indexes
        default['geo_point'] = {
            'type': 'Point',
            'coordinates': (default['lng'], default['lat'])
        }

        super().__init__(name, default=default, keys=('lng', 'lat', 'address'), **kwargs)

    @property
    def is_empty(self) -> bool:
        v = self.get_val()

        return (v['lng'], v['lat']) == (0.0, 0.0) or not v['address']

    def set_val(self, value: _Union[dict, _frozendict], **kwargs):
        """Hook.
        """
        if isinstance(value, _frozendict):
            value = dict(value)

        if isinstance(value, dict):
            # Checking lat and lng
            for k in ('lng', 'lat'):
                if k in value:
                    try:
                        value[k] = float(value[k])
                    except ValueError:
                        value[k] = 0.0
                else:
                    value[k] = 0.0

            # Checking address
            if 'address' in value and not isinstance(value['address'], str):
                raise ValueError("Field '{}.address': str expected.".format(self.name))

            # Checking address components
            if 'address_components' in value and not isinstance(value['address_components'], (list, tuple)):
                raise ValueError("Field '{}.address_components': list or tuple expected.".format(self.name))

            value['geo_point'] = {
                'type': 'Point',
                'coordinates': (value['lng'], value['lat']),
            }

        return super().set_val(value, **kwargs)
