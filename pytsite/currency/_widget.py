"""Currency Widgets
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import decimal as _decimal
from pytsite.core import widget as _widget, html as _html
from . import _functions


class Currency(_widget.input.Float):
    def __init__(self, currency: str=None, **kwargs):
        """Init.
        """
        super().__init__(**kwargs)

        if not currency:
            currency = _functions.get_main_currency()
        currency = currency.upper()

        self._currency = currency
        self._append = currency

    def set_value(self, value, **kwargs: dict):
        """Set value of the widget.
        """
        if not value:
            value = {'amount': 0.0, 'currency': _functions.get_main_currency()}

        if not isinstance(value, dict):
            raise ValueError('Dict expected.')

        value['amount'] = float(_decimal.Decimal(value['amount']).quantize(_decimal.Decimal('.01')))
        value['currency'] = value['currency'].upper()

        self._value = value

        return self

    def get_value(self, **kwargs: dict):
        if kwargs.get('validation_mode'):
            return self._value['amount']

        return self._value

    def render(self) -> _html.Element:
        r = super().render()
        r.append(_html.Input(type='hidden', name=self._uid + '[currency]', value=self._currency))
        new_uid = self.uid + '[amount]'

        text_input = r.get_child_by_uid(self._uid)
        text_input.set_attr('value', self._value['amount']).set_attr('uid', new_uid).set_attr('name', new_uid)

        return r
