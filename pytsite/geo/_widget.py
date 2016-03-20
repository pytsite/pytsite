"""Geo Widgets.
"""
from typing import Union as _Union
from frozendict import frozendict as _frozendict
from pytsite import assetman as _assetman, widget as _widget, html as _html

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Location(_widget.Base):
    """Geo Address Input Widget.
    """
    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        default = {
            'lng': 0.0,
            'lat': 0.0,
            'lng_lat': (0.0, 0.0),
            'accuracy': 0.0,
            'alt': 0.0,
            'alt_accuracy': 0.0,
            'heading': 0.0,
            'speed': 0.0,
        }

        super().__init__(uid, default=default, **kwargs)

        # Assets
        _assetman.add('pytsite.geo@js/widget/location.js')

        # CSS
        self._css += ' widget-geo-location'

    def set_val(self, val: _Union[dict, _frozendict], **kwargs):
        """Set value of the widget.
        """
        if val is None:
            self.clr_val()
            return

        if isinstance(val, _frozendict):
            val = dict(val)

        if not isinstance(val, dict):
            raise ValueError("Widget '{}': dict or None expected, while '{}' given.".format(self.name, repr(val)))

        if 'lat' not in val or 'lng' not in val:
            raise ValueError("Widget '{}': 'lat' and 'lng' keys are required.".format(self.uid))

        try:
            val['lng'] = float(val['lng'])
            val['lat'] = float(val['lat'])
        except ValueError:
            raise ValueError("Widget '{}': 'lat' and 'lng' keys should be floats.".format(self.uid))

        return super().set_val(val, **kwargs)

    def get_html_em(self) -> _html.Element:
        """Render the widget.
        """
        inputs = _html.TagLessElement()

        inputs.append(_html.P(cls='text'))

        for k in ('lng', 'lat', 'lng_lat', 'accuracy', 'alt', 'alt_accuracy', 'heading', 'speed'):
            inp_val = self._value[k] if k in self._value else ''
            inputs.append(_html.Input(type='hidden', cls=k, name=self._uid + '[' + k + ']', value=inp_val))

        return self._group_wrap(inputs)
