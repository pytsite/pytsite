"""Geo Widgets.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from json import dumps as _json_dumps, loads as _json_loads
from pytsite.core import assetman as _assetman, lang as _lang, widget as _widget, html as _html


class SearchAddress(_widget.base.Widget):
    """Geo Address Input Widget.
    """
    def __init__(self, **kwargs: dict):
        """Init.
        """
        super().__init__(**kwargs)

        lng = _lang.get_current_lang()
        _assetman.add_js('https://maps.googleapis.com/maps/api/js?libraries=places&language=' + lng)
        _assetman.add('pytsite.geo@js/address-input.js')

        self._group_cls += ' widget-geo-address-input'

    def set_value(self, val: dict, **kwargs: dict):
        """Set value of the widget.
        """
        if not isinstance(val, dict):
            raise ValueError('Dict expected.')

        if not val:
            return self

        for k in ['address', 'lng_lat', 'components']:
            if k not in val:
                raise ValueError("Value does not contain '{}'.".format(k))

        if not val['address'] or not val['lng_lat'] or not val['components']:
            return self

        lng_lat = _json_loads(val['lng_lat']) if isinstance(val['lng_lat'], str) else val['lng_lat']
        components = _json_loads(val['components']) if isinstance(val['components'], str) else val['components']

        value = {
            'address': val['address'],
            'lng_lat': lng_lat,
            'components': components
        }

        return super().set_value(value, **kwargs)

    def render(self) -> str:
        """Render the widget.
        """
        address_value = self._value['address'] if self._value else ''
        lng_lat_value = _json_dumps(self._value['lng_lat']) if self._value else ''
        components_value = _json_dumps(self._value['components']) if self._value else ''

        inputs = _html.Div()
        inputs.append(_html.Input(type='text', name=self._uid + '[search]', cls='form-control', value=address_value))
        inputs.append(_html.Input(type='hidden', name=self._uid + '[address]', value=address_value))
        inputs.append(_html.Input(type='hidden', name=self._uid + '[name]', value=address_value))
        inputs.append(_html.Input(type='hidden', name=self._uid + '[lng_lat]', value=lng_lat_value))
        inputs.append(_html.Input(type='hidden', name=self._uid + '[components]', value=components_value))

        return self._group_wrap(inputs)


class StaticMap(_widget.base.Widget):
    def __init__(self, **kwargs: dict):
        """Init.
        """
        super().__init__(**kwargs)

        self._language = _lang.get_current_lang()
        self._zoom = kwargs.get('zoom', 13)
        self._center = kwargs.get('center', '40.714728,-73.998672')
        self._width = kwargs.get('width', 320)
        self._height = kwargs.get('height', 240)
        self._markers = kwargs.get('markers', ({'location': self._center},))
        self._link_location = kwargs.get('link_location', '')

        self._group_cls += 'widget-geo-static-map'

    @property
    def language(self) -> str:
        return self._language

    def render(self) -> _html.Element:
        size = '{}x{}'.format(str(self._width), str(self._height))
        url = 'https://maps.googleapis.com/maps/api/staticmap?'
        url += 'center={}&zoom={}&size={}'.format(self._center, self._zoom, size)
        if self._markers:
            url += '&markers='
            for m in self._markers:
                url += m['location']
        img = _html.Img(src=url, cls='img-responsive')

        if self._link_location:
            img = img.wrap(_html.A(href='https://www.google.com/maps?q=' + self._link_location, target='_blank'))

        return self._group_wrap(img)