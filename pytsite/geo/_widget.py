"""Geo Widgets.
"""
from json import dumps as _json_dumps, loads as _json_loads
from pytsite import assetman as _assetman, widget as _widget, html as _html, lang as _lang
from . import _functions

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Location(_widget.Base):
    """Geo Address Input Widget.
    """
    def __init__(self, **kwargs):
        """Init.
        """
        super().__init__(**kwargs)

        _assetman.add('pytsite.geo@js/widget/location.js')
        self._group_cls += ' widget-geo-location'

    def set_value(self, val: dict, **kwargs: dict):
        """Set value of the widget.
        """
        if val is None:
            val = {}
        elif not isinstance(val, dict):
            raise ValueError('Dict expected.')

        return super().set_value(val, **kwargs)

    def render(self) -> _html.Element:
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
    def __init__(self, **kwargs):
        """Init.
        """
        super().__init__(**kwargs)

        self._autodetect = kwargs.get('autodetect', False)

        lng = _lang.get_current_lang()
        _assetman.add('https://maps.googleapis.com/maps/api/js?libraries=places&language=' + lng, 'js')
        _assetman.add('pytsite.geo@js/widget/address-input.js')

        self._group_cls = self._group_cls.replace('widget-geo-location', 'widget-geo-search-address')

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
            for k in ['lng', 'lat', 'address', 'address_components']:
                if k not in val:
                    raise ValueError("Value does not contain '{}' key.".format(k))

            if not val['lat'] or not val['lng'] or not val['address'] or not val['address_components']:
                return self

            components = _json_loads(val['address_components']) if isinstance(val['address_components'], str) \
                else val['address_components']

            val = {
                'address': val['address'],
                'lat': float(val['lat']),
                'lng': float(val['lng']),
                'address_components': components
            }

        return super().set_value(val, **kwargs)

    def get_value(self, **kwargs: dict):
        """Set value of the widget.
        """
        val = super().get_value(**kwargs)
        if not val:
            val = {
                'address': '',
                'lat': 0.0,
                'lng': 0.0,
                'address_components': []
            }

        return val

    def render(self) -> str:
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
    def __init__(self, lng: float=51.48, lat: float=0.0, query: str=None, **kwargs: dict):
        """Init.
        """
        super().__init__(**kwargs)

        self._language = kwargs.get('language', _lang.get_current_lang())
        self._lng = lng
        self._lat = lat
        self._query = query
        self._zoom = kwargs.get('zoom', 13)
        self._center = '%f,%f' % (self._lat, self._lng)
        self._width = kwargs.get('width', 320)
        self._height = kwargs.get('height', 240)
        self._link = kwargs.get('link', True)

        self._group_cls += ' widget-geo-static-map'

    @property
    def language(self) -> str:
        """Get language.
        """
        return self._language

    def render(self) -> _html.Element:
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
