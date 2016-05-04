"""PytSite Wallet Widgets
"""
from decimal import Decimal as _Decimal
from frozendict import frozendict as _frozendict
from pytsite import widget as _w, odm as _odm, auth as _auth, currency as _currency, html as _html

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class AccountSelect(_w.select.Select):
    """Wallet Account Select Widget
    """
    def __init__(self, uid: str, **kwargs):
        u = _auth.get_current_user()
        items = []

        if u.has_permission('pytsite.odm_ui.browse.wallet_account') or \
                u.has_permission('pytsite.odm_ui.browse_own.wallet_account'):
            f = _odm.find('wallet_account').sort([('title', _odm.I_ASC)])

            # User can only view its own accounts
            if not u.has_permission('pytsite.odm_ui.browse.wallet_account'):
                f.where('owner', '=', u)

            for acc in f.get():
                label = '{} ({})'.format(acc.title, acc.currency)
                items.append(('wallet_account:' + str(acc.id), label))

        super().__init__(uid, items=items, **kwargs)


class MoneyInput(_w.input.Decimal):
    """Money Input Widget
    """
    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        self._default_currency = kwargs.get('default_currency', _currency.get_main())
        if self._default_currency not in _currency.get_all():
            raise _currency.error.CurrencyNotDefined("Currency '{}' is not defined.".format(self._default_currency))

        super().__init__(uid, **kwargs)

        self._assets.append('pytsite.wallet@js/widget-money-input.js')

    def set_val(self, value: dict, **kwargs):
        """Set value of the widget.
        """
        # 'Empty' value
        if value is None:
            value = {'amount': _Decimal('0.0'), 'currency': self._default_currency}

        # Checking input
        if type(value) not in (dict, _frozendict):
            raise ValueError('Dict expected.')

        # Convert input to mutable dict
        if isinstance(value, _frozendict):
            value = dict(value)

        # Checking input parts
        if 'currency' not in value or not value['currency']:
            raise ValueError("Value of the widget '{}' must contain 'currency' key.".format(self._name))
        if 'amount' not in value:
            raise ValueError("Value of the widget '{}' must contain 'amount' key.".format(self._name))

        # Checking currency validness
        if value['currency'] not in _currency.get_all():
            raise _currency.error.CurrencyNotDefined("Currency '{}' is not defined.".format(value['currency']))

        # Processing string input
        if isinstance(value['amount'], str) and not value['amount'].strip():
            value['amount'] = _Decimal(0)

        # Processing float input
        if isinstance(value['amount'], float):
            value['amount'] = str(value['amount'])

        # Processing another inputs
        if not isinstance(value['amount'], _Decimal):
            value['amount'] = _Decimal(value['amount'])

        self._value = _frozendict(value)

        return self

    def get_val(self, **kwargs) -> _frozendict:
        """Get value of the widget.
        """
        if kwargs.get('mode') == 'validation':
            return self._value['amount']

        return self._value

    def get_html_em(self, **kwargs) -> _html.Element:
        """Get HTML element of the widget.
        :param **kwargs:
        """
        self._append = _currency.get_symbol(self._value['currency'])

        r = super().get_html_em()
        r.append(_html.Input(type='hidden', name=self._uid + '[currency]', value=self._value['currency']))

        new_uid = self.uid + '[amount]'
        text_input = r.get_child_by_uid(self._uid)
        text_input.set_attr('value', round(self._value['amount'], 2))
        text_input.set_attr('uid', new_uid)
        text_input.set_attr('name', new_uid)

        return r
