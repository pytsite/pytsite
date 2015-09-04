"""Currency ODM Classes.
"""
import decimal as _decimal
from pytsite import odm as _odm
from . import _functions

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Currency(_odm.field.Abstract):
    def set_val(self, value, change_modified: bool=True, **kwargs):
        """Set value of the field.

        :param value: dict, float, int, str
        """
        if isinstance(value, dict):
            # Checking for necessary keys
            for req in ['amount', 'currency']:
                if req not in value:
                    raise ValueError("'{}' is not in value.".format(req))

            # Checking if the currency is valid
            if value['currency'] not in _functions.get_currencies():
                raise ValueError("{} is not a valid currency.".format(value['currency']))

            # Quantize amount and convert it to float
            value['amount'] = float(_decimal.Decimal(value['amount']).quantize(_decimal.Decimal('.01')))

        elif type(value) in (float, int, str):
            value = {'amount': value, 'currency': _functions.get_main_currency()}

        elif value is not None:
            raise ValueError("Field '{}': dictionary, float, integer or string expected.".format(self.name))

        return super().set_val(value, change_modified, **kwargs)
