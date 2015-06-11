"""Geo Widgets.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core.widgets.input import TextInputWidget
from pytsite.core import assetman, lang


class GeoAddressInputWidget(TextInputWidget):

    def __init__(self, **kwargs: dict):
        """Init.
        """
        super().__init__(**kwargs)

        lng = lang.get_current_lang()
        assetman.add_js('https://maps.googleapis.com/maps/api/js?libraries=places&language=' + lng)
        assetman.add('pytsite.geo@js/address-input.js')

        self._group_cls = self._group_cls.replace('widget-text-input', 'widget-geo-address-input')
        self._name = self._uid + '[search]'

    def set_value(self, value, **kwargs: dict):
        """Set value of the widget.
        """
        self._value = value

        return self