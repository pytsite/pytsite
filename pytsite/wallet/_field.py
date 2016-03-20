"""PytSite Money ODM Field
"""
from frozendict import frozendict as _frozendict
from decimal import Decimal as _Decimal
from pytsite import odm as _odm, currency as _currency, auth as _auth

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Money(_odm.field.Abstract):
    """PytSite Money ODM Field
    """
    def __init__(self, name: str, **kwargs):
        """Init.
        """
        # Default value
        if not kwargs.get('default'):
            u = _auth.get_current_user()
            currency = u.f_get('currency') if u and u.has_field('currency') else _currency.get_main()
            kwargs['default'] = {'currency': currency, 'amount': _Decimal('0.0')}

        super().__init__(name, **kwargs)

    def set_val(self, value: dict, **kwargs):
        """Set value fo the field.
        """
        # Reset value to default
        if value is None:
            self.clr_val(**kwargs)
            return

        # Convert to mutable dict if necessary
        if isinstance(value, _frozendict):
            value = dict(value)

        # Check value type
        if not isinstance(value, dict):
            raise TypeError("Value of the field '{}' should be a dict.".format(self._name))

        # Check for required dict keys
        if 'currency' not in value or not value['currency']:
            raise ValueError("Value of the field '{}' must contain 'currency' key.".format(self._name))
        if 'amount' not in value:
            raise ValueError("Value of the field '{}' must contain 'amount' key.".format(self._name))

        # Check for currency validness
        if value['currency'] not in _currency.get_all():
            raise _currency.error.CurrencyNotDefined("Currency '{}' is not defined.".format(value['currency']))

        # Float amount should be converted to string before converting to Decimal
        if isinstance(value['amount'], float):
            value['amount'] = str(value['amount'])

        # Convert amount to Decimal
        if not isinstance(value['amount'], _Decimal):
            value['amount'] = _Decimal(value['amount'])

        # Convert to immutable dict and set
        super().set_val(_frozendict(value), **kwargs)

    def get_val(self, **kwargs) -> _frozendict:
        """Get value of the field.
        """
        return super().get_val(**kwargs)

    def get_storable_val(self):
        """Get storable value of the feld.
        """
        v = self.get_val()
        return {
            'currency': v['currency'],
            'currency_symbol': _currency.get_symbol(v['currency']),
            'currency_title': _currency.get_title(v['currency']),
            'amount': float(v['amount'])
        }
