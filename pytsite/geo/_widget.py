"""Geo Widgets.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from json import dumps as _json_dumps, loads as _json_loads
from pytsite.core import assetman as _assetman, lang as _lang, widget as _widget, html as _html
from . import _functions


class Location(_widget.Base):
    """Geo Address Input Widget.
    """
    def __init__(self, **kwargs):
        """Init.
        """
        super().__init__(**kwargs)

        _assetman.add('pytsite.geo@js/widget/location.js')
        self._group_cls += ' widget geo location'

    def render(self) -> _html.Element:
        """Render the widget.
        """
        return self._group_wrap(_html.TagLessElement())


class SearchAddress(Location):
    """Geo Address Input Widget.
    """
    def __init__(self, **kwargs):
        """Init.
        """
        super().__init__(**kwargs)

        self._autodetect = kwargs.get('autodetect', False)

        lng = _lang.get_current_lang()
        _assetman.add('https://maps.googleapis.com/maps/api/js?libraries=places&language=' + lng, 'js')
        _assetman.add('pytsite.geo@js/widget/address-input.js')

        self._group_cls = self._group_cls.replace('location', 'search-address')

    @property
    def autodetect(self) -> bool:
        return self._autodetect

    @autodetect.setter
    def autodetect(self, value: bool):
        self._autodetect = value

    def set_value(self, val: dict, **kwargs: dict):
        """Set value of the widget.
        """
        if not isinstance(val, dict):
            raise ValueError('Dict expected.')

        if val:
            for k in ['address', 'lng_lat', 'components']:
                if k not in val:
                    raise ValueError("Value does not contain '{}'.".format(k))

            if not val['address'] or not val['lng_lat'] or not val['components']:
                return self

            lng_lat = _json_loads(val['lng_lat']) if isinstance(val['lng_lat'], str) else val['lng_lat']
            components = _json_loads(val['components']) if isinstance(val['components'], str) else val['components']

            val = {
                'address': val['address'],
                'lng_lat': lng_lat,
                'components': components
            }

        return super().set_value(val, **kwargs)

    def render(self) -> str:
        """Render the widget.
        """
        address_value = self._value['address'] if self._value else ''
        lng_lat_value = _json_dumps(self._value['lng_lat']) if self._value else ''
        components_value = _json_dumps(self._value['components']) if self._value else ''

        inputs = _html.TagLessElement()
        inputs.append(_html.Input(type='text', name=self._uid + '[search]', cls='form-control', value=address_value))
        inputs.append(_html.Input(type='hidden', name=self._uid + '[address]', value=address_value))
        inputs.append(_html.Input(type='hidden', name=self._uid + '[lng_lat]', value=lng_lat_value))
        inputs.append(_html.Input(type='hidden', name=self._uid + '[components]', value=components_value))

        self._data['autodetect'] = int(self._autodetect)

        return self._group_wrap(inputs)


class StaticMap(_widget.Base):
    def __init__(self, **kwargs: dict):
        """Init.
        """
        super().__init__(**kwargs)

        self._language = kwargs.get('language', _lang.get_current_lang())
        self._zoom = kwargs.get('zoom', 13)
        self._lat = kwargs.get('lat', 51.48)
        self._lng = kwargs.get('lng', 0.0)
        self._center = '%f,%f' % (self._lat, self._lng)
        self._width = kwargs.get('width', 320)
        self._height = kwargs.get('height', 240)
        self._address = kwargs.get('address', '')
        self._link = kwargs.get('link', True)

        self._group_cls += 'widget-geo-static-map'

    @property
    def language(self) -> str:
        return self._language

    def render(self) -> _html.Element:
        size = '{}x{}'.format(str(self._width), str(self._height))
        url = 'https://maps.googleapis.com/maps/api/staticmap?'
        url += 'center={}&zoom={}&size={}'.format(self._center, self._zoom, size)
        url += '&markers=' + self._center
        img = _html.Img(src=url, cls='img-responsive')

        if self._link:
            link = _functions.get_map_link(self._address, self._lat, self._lng)
            img = img.wrap(_html.A(href=link, target='_blank', title=_lang.t('geo@show_on_map')))

        return self._group_wrap(img)
