"""Geo ODM Fields.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core import odm as _odm


class Location(_odm.field.Dict):
    """Geo Location Field.
    """
    def __init__(self, name, **kwargs):
        """Init.
        """
        super().__init__(name, keys=('accuracy', 'alt', 'alt_accuracy', 'heading', 'speed'),
                         nonempty_keys=('lat', 'lng'), **kwargs)

    def set_val(self, value: dict, change_modified: bool=True, **kwargs):
        """Hook.
        """
        for k in ('lng', 'lat', 'accuracy', 'alt', 'alt_accuracy', 'heading', 'speed'):
            if k in value:
                try:
                    value[k] = float(value[k])
                except ValueError:
                    value[k] = 0.0
            else:
                value[k] = 0.0

        value['lng_lat'] = [value['lng'], value['lat']]

        if 'address' not in value:
            value['address'] = ''

        if 'address_components' not in value:
            value['address_components'] = []

        return super().set_val(value, change_modified, **kwargs)
