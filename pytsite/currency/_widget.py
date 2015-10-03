"""Currency Widgets
"""
import decimal as _decimal
from pytsite import html as _html, widget as _widget
from . import _functions

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


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
            raise ValueError("Widget '{}': dict expected, while '{}' given.".format(self.uid, repr(value)))

        for k in ('amount', 'currency'):
            if k not in value:
                raise ValueError("Widget '{}': '{}' is not in the value.".format(self.uid, k))

        if not value['amount']:
            value['amount'] = 0.0

        if not value['currency']:
            value['currency'] = _functions.get_main_currency()

        if value['currency'] not in _functions.get_currencies():
            raise ValueError("Widget '{}': '{}' is not a valid currency.".format(self.uid, value['currency']))

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
