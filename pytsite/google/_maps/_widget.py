"""PytSite Google Widgets.
"""
from typing import Union as _Union
from copy import deepcopy as _deepcopy
from json import dumps as _json_dumps, loads as _json_loads
from frozendict import frozendict as _frozendict
from pytsite import widget as _pytsite_widget, browser as _browser, html as _html, reg as _reg, geo as _geo, \
    validation as _validation

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class AddressInput(_pytsite_widget.Base):
    """Geo Address Input Widget.
    """

    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        maps_libs = _reg.get('google.maps.libraries', [])
        if 'places' not in maps_libs:
            raise RuntimeError("You should include 'places' in your 'google.maps.libraries' configuration.")

        if 'default' not in kwargs:
            kwargs['default'] = {
                'address': '',
                'lng': 0.0,
                'lat': 0.0,
                'address_components': ()
            }

        super().__init__(uid, **kwargs)

        # Geo based auto detection
        self._autodetect = kwargs.get('autodetect', False)

        # CSS
        self._css += ' widget-google-address-input'

        # Assets
        self.assets.extend(_browser.get_assets('google-maps'))
        self.assets.append('pytsite.google@js/widget/address-input.js')

        # Validation rule for 'required' widget
        if self._required:
            self.clr_rules().add_rules([r for r in self.get_rules() if not isinstance(r, _validation.rule.NonEmpty)])
            self.add_rule(_geo.validation_rule.AddressNonEmpty())

    @property
    def required(self) -> bool:
        return self._required

    @required.setter
    def required(self, value: bool):
        if value:
            self.add_rule(_geo.validation_rule.AddressNonEmpty())
        else:
            # Clear all added NonEmpty and AddressNonEmpty rules
            rules = [r for r in self.get_rules() if not isinstance(r, (
                _validation.rule.NonEmpty,
                _geo.validation_rule.AddressNonEmpty
            ))]
            self.clr_rules().add_rules(rules)

        self._required = value

    @property
    def autodetect(self) -> bool:
        return self._autodetect

    @autodetect.setter
    def autodetect(self, value: bool):
        self._autodetect = value

    def set_val(self, val: _Union[dict, _frozendict], **kwargs):
        """Set value of the widget.
        """
        if isinstance(val, (dict, _frozendict)) and val:
            # Checking for required keys
            for k in ['lng', 'lat', 'address', 'address_components']:
                if k not in val:
                    raise ValueError("Value does not contain '{}' key.".format(k))

            # Loading address components
            if isinstance(val['address_components'], str):
                components = _json_loads(val['address_components'])
            else:
                components = val['address_components']

            val = {
                'address': val['address'],
                'lng': float(val['lng']),
                'lat': float(val['lat']),
                'address_components': components
            }
        elif val is None:
            val = self._default
        else:
            raise ValueError('Dict or None expected.')

        return super().set_val(val, **kwargs)

    def get_val(self, **kwargs):
        """Set value of the widget.
        """
        return super().get_val(**kwargs) or _deepcopy(self._default)

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

        self._data['autodetect'] = self._autodetect

        return self._group_wrap(inputs)
