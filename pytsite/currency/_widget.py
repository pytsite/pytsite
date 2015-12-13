"""Currency Widgets
"""
import decimal as _decimal
from pytsite import html as _html, widget as _widget
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Select(_widget.select.Select):
    def __init__(self, uid: str, **kwargs):
        super().__init__(uid, **kwargs)

        items = _api.get_all()
        self._items = zip(items, items)


class Input(_widget.input.Float):
    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        super().__init__(uid, **kwargs)

        currency = kwargs.get('currency', _api.get_main()).upper()
        if currency not in _api.get_all():
            raise ValueError("Widget '{}': '{}' is not a valid currency.".format(self.uid, currency))

        self._currency = currency
        self._append = currency
        self._value = {'amount': 0.0, 'currency': self._currency}

        # Remove validation rules which defined in super class
        self.remove_rules()

    def set_val(self, value, **kwargs):
        """Set value of the widget.
        """
        if value is None:
            return

        if isinstance(value, dict) and 'amount' in value:
            amount = float(value['amount'])
        elif isinstance(value, tuple) and value:
            amount = float(value[0])
        else:
            amount = float(value)

        self._value['amount'] = float(_decimal.Decimal(amount).quantize(_decimal.Decimal('.01')))

        return self

    def get_val(self, **kwargs):
        if kwargs.get('validation_mode'):
            return self._value['amount']

        return self._value

    def get_html_em(self) -> _html.Element:
        r = super().get_html_em()
        r.append(_html.Input(type='hidden', name=self._uid + '[currency]', value=self._currency))
        new_uid = self.uid + '[amount]'

        text_input = r.get_child_by_uid(self._uid)
        text_input.set_attr('value', self._value['amount']).set_attr('uid', new_uid).set_attr('name', new_uid)

        return r
