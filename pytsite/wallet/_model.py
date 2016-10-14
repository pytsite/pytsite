"""PytSite Wallet Package Models.
"""
from typing import Iterable as _Iterable
from datetime import datetime as _datetime
from decimal import Decimal as _Decimal
from pytsite import odm as _odm, odm_ui as _odm_ui, currency as _currency, auth as _auth, widget as _widget, \
    errors as _errors, auth_storage_odm as _auth_storage_odm
from . import _error, _widget as _wallet_widget

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_main_currency = _currency.get_main()


class Account(_odm_ui.model.UIEntity):
    """Wallet ODM Model.
    """

    def _setup_fields(self):
        """Hook.
        """
        self.define_field(_odm.field.String('currency', required=True))
        self.define_field(_odm.field.String('title', required=True))
        self.define_field(_odm.field.Decimal('balance', round=8))
        self.define_field(_auth_storage_odm.field.User('owner', required=True))
        self.define_field(_odm.field.RefsUniqueList('pending_transactions', model='wallet_transaction'))
        self.define_field(_odm.field.RefsUniqueList('cancelling_transactions', model='wallet_transaction'))
        self.define_field(_odm.field.Dict('options'))

    def _setup_indexes(self):
        """Hook.
        """
        self.define_index([('title', _odm.I_ASC)], True)

    @property
    def currency(self) -> str:
        return self.f_get('currency')

    @property
    def title(self) -> str:
        return self.f_get('title')

    @property
    def balance(self) -> _Decimal:
        return self.f_get('balance')

    @property
    def owner(self) -> _auth.model.AbstractUser:
        return self.f_get('owner')

    @property
    def pending_transactions(self):
        """
        :rtype: _Iterable[Transaction]
        """
        return self.f_get('pending_transactions')

    @property
    def cancelling_transactions(self):
        """
        :rtype: _Iterable[Transaction]
        """
        return self.f_get('cancelling_transactions')

    @property
    def options(self) -> dict:
        return self.f_get('options')

    def _on_f_set(self, field_name: str, value, **kwargs):
        if field_name == 'currency' and value not in _currency.get_all():
            raise _currency.error.CurrencyNotDefined("Currency '{}' is not defined.".format(value))

        return super()._on_f_set(field_name, value, **kwargs)

    def _pre_delete(self, **kwargs):
        """Hook.

        :param force: only for testing purposes.
        """
        if not kwargs.get('force'):
            f = _odm.find('wallet_transaction').or_eq('source', self).or_eq('destination', self)
            if f.count():
                raise _errors.ForbidDeletion('Cannot delete account due to its usage in transaction(s).')

    @classmethod
    def odm_ui_browser_setup(cls, browser):
        """Setup ODM UI browser hook.

        :type browser: pytsite.odm_ui._browser.Browser
        """
        browser.data_fields = [
            ('_id', 'pytsite.wallet@id'),
            ('title', 'pytsite.wallet@title'),
            ('currency', 'pytsite.wallet@currency'),
            ('balance', 'pytsite.wallet@balance'),
            ('owner', 'pytsite.wallet@owner'),
        ]

    def odm_ui_browser_row(self) -> tuple:
        """Get single UI browser row hook.
        """
        balance = _currency.fmt(self.currency, self.balance)
        owner = self.owner if self.owner else _auth.get_first_admin_user()

        return str(self.id), self.title, self.currency, balance, owner.full_name

    def odm_ui_mass_action_entity_description(self) -> str:
        return '{} ({}, {})'.format(self.title, str(self.id), self.currency)

    def odm_ui_m_form_setup_widgets(self, frm):
        """Modify form setup hook.

        :type frm: pytsite.form.Form
        """
        frm.add_widget(_widget.input.Text(
            uid='title',
            weight=10,
            label=self.t('title'),
            value=self.title,
            required=True,
        ))
        frm.add_rule('title', _odm.validation.FieldUnique(
            model='wallet_account',
            field='title',
            exclude_ids=self.id if not self.is_new else None,
        ))

        if self.is_new:
            frm.add_widget(_currency.widget.Select(
                uid='currency',
                weight=20,
                label=self.t('currency'),
                required=True,
                value=self.currency,
                h_size='col-sm-4 col-md-3 col-lg-2',
            ))
        else:
            frm.add_widget(_widget.static.Text(
                uid='currency',
                weight=20,
                label=self.t('currency'),
                title=self.currency,
                value=self.currency,
            ))

        frm.add_widget(_auth.widget.UserSelect(
            uid='owner',
            weight=30,
            label=self.t('owner'),
            required=True,
            value=self.owner,
            h_size='col-sm-6 col-md-5 col-lg-4',
        ))


class Transaction(_odm_ui.model.UIEntity):
    """Transaction ODM Model.
    """

    def _setup_fields(self):
        """Hook.
        """
        self.define_field(_odm.field.DateTime('time', required=True, default=_datetime.now()))
        self.define_field(_odm.field.Ref('source', model='wallet_account', required=True))
        self.define_field(_odm.field.Ref('destination', model='wallet_account', required=True))
        self.define_field(_odm.field.String('state', default='new'))
        self.define_field(_odm.field.Decimal('amount', round=8))
        self.define_field(_odm.field.Decimal('exchange_rate', round=8, default=1))
        self.define_field(_odm.field.String('description'))
        self.define_field(_odm.field.Dict('options'))

    def _setup_indexes(self):
        """Hook.
        """
        self.define_index([('time', _odm.I_DESC)])

    @property
    def time(self) -> _datetime:
        return self.f_get('time')

    @property
    def source(self) -> Account:
        return self.f_get('source')

    @property
    def destination(self) -> Account:
        return self.f_get('destination')

    @property
    def state(self) -> str:
        return self.f_get('state')

    @property
    def amount(self) -> _Decimal:
        return self.f_get('amount')

    @property
    def exchange_rate(self) -> _Decimal:
        return self.f_get('exchange_rate')

    @property
    def description(self) -> str:
        return self.f_get('description')

    @property
    def options(self) -> dict:
        return self.f_get('options')

    def _on_f_set(self, field_name: str, value, **kwargs):
        """Hook.
        """
        if not self.is_new and field_name in ('source', 'destination', 'amount'):
            raise ValueError('Transaction cannot be changed.')

        return super()._on_f_set(field_name, value, **kwargs)

    def _pre_save(self, **kwargs):
        """Hook.
        """
        super()._pre_save(**kwargs)

        if self.is_new and self.exchange_rate == 1:
            self.f_set('exchange_rate', _currency.get_rate(self.source.currency, self.destination.currency))

    def _pre_delete(self, **kwargs):
        """Hook.
        :param force: only for testing purposes.
        """
        if not kwargs.get('force'):
            raise _errors.ForbidDeletion('Wallet transactions cannot be deleted.')

    def cancel(self):
        if self.state != 'committed':
            raise _error.ImproperTransactionState('It is possible to cancel only committed transactions.')

        with self:
            self.f_set('state', 'cancel').save()

        return self

    @classmethod
    def odm_ui_browser_setup(cls, browser):
        """Setup ODM UI browser hook.

        :type browser: pytsite.odm_ui._browser.Browser
        """
        browser.data_fields = [
            ('time', 'pytsite.wallet@time'),
            ('description', 'pytsite.wallet@description'),
            ('source', 'pytsite.wallet@source'),
            ('destination', 'pytsite.wallet@destination'),
            ('amount', 'pytsite.wallet@amount'),
            ('state', 'pytsite.wallet@state'),
        ]
        browser.default_sort_field = 'time'

    @classmethod
    def odm_ui_browser_mass_action_buttons(cls) -> tuple:
        return {'ep': 'pytsite.wallet@transactions_cancel',
                'icon': 'undo',
                'color': 'danger',
                'title': Transaction.t('odm_ui_form_title_delete_wallet_transaction')},

    def odm_ui_browser_row(self) -> tuple:
        """Get single UI browser row hook.
        """
        time = self.f_get('time', fmt='pretty_date_time')
        source = self.source.title
        destination = self.destination.title
        amount = _currency.fmt(self.source.currency, self.amount)
        if self.source.currency != self.destination.currency:
            amount += ' ({})'.format(_currency.fmt(self.destination.currency, self.amount * self.exchange_rate))

        state_cls = 'primary'
        if self.state in ('pending', 'cancel', 'cancelling'):
            state_cls = 'warning'
        if self.state == 'committed':
            state_cls = 'success'
        if self.state == 'cancelled':
            state_cls = 'default'
        state = '<span class="label label-{}">'.format(state_cls) + self.t('transaction_state_' + self.state) + '</div>'

        return time, self.description, source, destination, amount, state

    def odm_ui_browser_entity_actions(self) -> tuple:
        if self.state == 'committed':
            return {'icon': 'undo',
                    'ep': 'pytsite.wallet@transactions_cancel',
                    'color': 'danger',
                    'title': self.t('cancel')},

        return ()

    def odm_ui_m_form_setup_widgets(self, frm):
        """Modify form setup hook.

        :type frm: pytsite.form.Form
        """
        frm.add_widget(_wallet_widget.AccountSelect(
            uid='source',
            weight=10,
            label=self.t('source'),
            required=True,
            value=self.source,
        ))

        frm.add_widget(_wallet_widget.AccountSelect(
            uid='destination',
            weight=20,
            label=self.t('destination'),
            required=True,
            value=self.destination,
        ))

        frm.add_widget(_widget.input.Decimal(
            uid='amount',
            weight=30,
            label=self.t('amount'),
            value=self.amount,
            required=True,
            min=0.01,
            h_size='col-sm-4 col-md-3 col-lg-2',
        ))

        frm.add_widget(_widget.input.Text(
            uid='description',
            weight=40,
            label=self.t('description'),
            value=self.description,
            required=True,
        ))
