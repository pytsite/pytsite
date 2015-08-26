"""Currency ODM Classes.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import decimal as _decimal

from pytsite import odm as _odm
from . import _functions


class CurrencyField(_odm.field.Abstract):
    def set_val(self, value: dict, change_modified: bool=True, **kwargs):
        """Set value of the field.
        """
        if value is None:
            return

        if not isinstance(value, dict):
            raise ValueError('Dict expected.')

        for req in ['amount', 'currency']:
            if req not in value:
                raise ValueError("'{}' is not in value.".format(req))

        value['amount'] = float(value['amount'])

        if value['currency'] not in _functions.get_currencies():
            raise ValueError("{} is not valid currency.".format(value['currency']))

        value['amount'] = float(_decimal.Decimal(value['amount']).quantize(_decimal.Decimal('.01')))

        return super().set_val(value, change_modified, **kwargs)
