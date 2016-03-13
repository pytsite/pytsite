"""Geo Widgets.
"""
from typing import Union as _Union
from json import dumps as _json_dumps, loads as _json_loads
from decimal import Decimal as _Decimal
from pytsite import assetman as _assetman, widget as _widget, html as _html, lang as _lang
from . import _functions

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class LngLat(_widget.Base):
    """Latitude/longitude widget.

    This widget intended to use in cases where you need to fetch/store pair of geo coordinates.
    """
    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        super().__init__(uid, **kwargs)

        _assetman.add('pytsite.geo@js/widget/lng-lat.js')
        self._css += ' widget-geo-lng-lat'

    def set_val(self, val: _Union[None, list, tuple, str], **kwargs):
        """Set value of the widget.
        """
        if val is None:
            val = (_Decimal('0.0'), _Decimal('0.0'))
        elif isinstance(val, str):
            val = _json_loads(val)

        if type(val) not in (list, tuple):
            raise ValueError("Widget '{}': list, tuple, str or None expected, but '{}' given.".
                             format(self.name, repr(val)))

        if len(val) != 2:
            raise ValueError("Widget '{}': value must contain exact 2 items.".format(self.name))

        valid_types = (float, _Decimal)
        if type(val[0]) not in valid_types or type(val[1]) not in valid_types:
            raise TypeError("Widget '{}': value must contain only float or decimal items.".format(self.name))

        val = (round(_Decimal(val[0]), 6), round(_Decimal(val[1]), 6))

        return super().set_val(val, **kwargs)

    def get_html_em(self) -> _html.Element:
        """Render the widget.
        """
        v = (float(self.get_val()[0]), float(self.get_val()[1]))
        w = _html.TagLessElement()
        w.append(_html.P('Longitude: {}, latitude: {}'.format(v[0], v[1]), cls='form-control-static'))
        w.append(_html.Input(type='hidden', uid=self._uid, name=self._uid, value=_json_dumps(v)))

        return self._group_wrap(w)


class Location(_widget.Base):
    """Geo Address Input Widget.
    """
    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        super().__init__(uid, **kwargs)

        _assetman.add('pytsite.geo@js/widget/location.js')
        self._css += ' widget-geo-location'

    def set_val(self, val: dict, **kwargs):
        """Set value of the widget.
        """
        if val is None:
            val = {}

        if not isinstance(val, dict):
            raise ValueError("Widget '{}': dict or None expected, while '{}' given.".format(self.name, repr(val)))

        return super().set_val(val, **kwargs)

    def get_html_em(self) -> _html.Element:
        """Render the widget.
        """
        inputs = _html.TagLessElement()
        for k in ('lng', 'lat', 'lng_lat', 'accuracy', 'alt', 'alt_accuracy', 'heading', 'speed'):
            inp_val = self._value[k] if k in self._value else ''
            inputs.append(_html.Input(type='hidden', cls=k, name=self._uid + '[' + k + ']', value=inp_val))

        return self._group_wrap(inputs)


class SearchAddress(Location):
    """Geo Address Input Widget.
    """
    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        super().__init__(uid, **kwargs)

        self._autodetect = kwargs.get('autodetect', False)

        lng = _lang.get_current()
        _assetman.add('https://maps.googleapis.com/maps/api/js?libraries=places&amp;language=' + lng, 'js')
        _assetman.add('pytsite.geo@js/widget/address-input.js')

        self._css = self._css.replace('widget-geo-location', 'widget-geo-search-address')

    @property
    def autodetect(self) -> bool:
        return self._autodetect

    @autodetect.setter
    def autodetect(self, value: bool):
        self._autodetect = value

    def set_val(self, val: dict, **kwargs):
        """Set value of the widget.
        """
        if isinstance(val, dict) and val:
            for k in ['lng', 'lat', 'address', 'address_components']:
                if k not in val:
                    raise ValueError("Value does not contain '{}' key.".format(k))

            if not val['lat'] or not val['lng'] or not val['address'] or not val['address_components']:
                return self

            components = _json_loads(val['address_components']) if isinstance(val['address_components'], str) \
                else val['address_components']

            val = {
                'address': val['address'],
                'lng': float(val['lng']),
                'lat': float(val['lat']),
                'address_components': components
            }

        elif val is not None:
            raise ValueError('Dict or None expected.')

        return super().set_val(val, **kwargs)

    def get_val(self, **kwargs):
        """Set value of the widget.
        """
        val = super().get_val(**kwargs)
        if not val:
            val = {
                'address': '',
                'lng': 0.0,
                'lat': 0.0,
                'address_components': []
            }

        return val

    def get_html_em(self) -> str:
        """Render the widget.
        """
        lng = self.value['lng']
        lat = self.value['lat']
        address = self.value['address']
        address_components = _json_dumps(self.value['address_components'])

        inputs = _html.TagLessElement()
        inputs.append(_html.Input(type='text', name=self._uid + '[search]', cls='form-control', value=address))
        inputs.append(_html.Input(type='hidden', name=self._uid + '[lng]', value=lng))
        inputs.append(_html.Input(type='hidden', name=self._uid + '[lat]', value=lat))
        inputs.append(_html.Input(type='hidden', name=self._uid + '[address]', value=address))
        inputs.append(_html.Input(type='hidden', name=self._uid + '[address_components]', value=address_components))

        self._data['autodetect'] = int(self._autodetect)

        return self._group_wrap(inputs)


class StaticMap(_widget.Base):
    """Static Map Widget.
    """
    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        super().__init__(uid, **kwargs)

        self._language = kwargs.get('language', _lang.get_current())
        self._lng = kwargs.get('lng', 50.45)
        self._lat = kwargs.get('lat', 30.523333)
        self._query = kwargs.get('query')
        self._zoom = kwargs.get('zoom', 15)
        self._center = '%f,%f' % (self._lat, self._lng)
        self._width = kwargs.get('width', 640)
        self._height = kwargs.get('height', 320)
        self._link = kwargs.get('link', True)

        self._css += ' widget-geo-static-map'

    @property
    def language(self) -> str:
        """Get language.
        """
        return self._language

    def get_html_em(self) -> _html.Element:
        """Render the widget.
        """
        if not self._lat and not self._lng:
            return _html.TagLessElement()

        size = '{}x{}'.format(str(self._width), str(self._height))
        url = 'https://maps.googleapis.com/maps/api/staticmap?'
        url += 'center={}&zoom={}&size={}'.format(self._center, self._zoom, size)
        url += '&markers=' + self._center
        img = _html.Img(src=url, cls='img-responsive')

        if self._link:
            link = _functions.get_map_link(self._lng, self._lat, self._query)
            img = img.wrap(_html.A(href=link, target='_blank', title=_lang.t('pytsite.geo@show_on_map')))

        return self._group_wrap(img)
