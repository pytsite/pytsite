"""Geo Widgets.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from json import dumps as json_dumps, loads as json_loads
from pytsite.core import assetman, lang
from pytsite.core.widgets.abstract import AbstractWidget
from pytsite.core.html import Input


class GeoAddressInputWidget(AbstractWidget):
    """Geo Address Input Widget.
    """

    def __init__(self, **kwargs: dict):
        """Init.
        """
        super().__init__(**kwargs)

        lng = lang.get_current_lang()
        assetman.add_js('https://maps.googleapis.com/maps/api/js?libraries=places&language=' + lng)
        assetman.add('pytsite.geo@js/address-input.js')

        self._group_cls += ' widget-geo-address-input'

    def set_value(self, val: dict, **kwargs: dict):
        """Set value of the widget.
        """
        if not isinstance(val, dict):
            raise ValueError('Dict expected.')

        if not val:
            self._value = {
                'address': '',
                'name': '',
                'lat_lng': [0.0, 0.0],
                'components': [],
            }
            return

        for k in ['address', 'name', 'lat_lng']:
            if k not in val:
                raise ValueError("Value does not contain '{}'.".format(k))

        lat_lng = json_loads(val['lat_lng']) if isinstance(val['lat_lng'], str) else val['lat_lng']
        components = json_loads(val['components']) if isinstance(val['components'], str) else val['components']

        self._value = {
            'address': val['address'],
            'name': val['name'],
            'lat_lng': lat_lng,
            'components': components
        }

    def render(self) -> str:
        """Render the widget.
        """
        inputs = [
            Input(type='text', name=self._uid + '[search]', cls='form-control', value=self._value['address']),
            Input(type='hidden', name=self._uid + '[address]', value=self._value['address']),
            Input(type='hidden', name=self._uid + '[name]', value=self._value['name']),
            Input(type='hidden', name=self._uid + '[lat_lng]', value=json_dumps(self._value['lat_lng'])),
            Input(type='hidden', name=self._uid + '[components]', value=json_dumps(self._value['components'])),
        ]

        r_inputs = ''
        for v in inputs:
            r_inputs += v.render()

        return self._group_wrap(r_inputs)