"""PytSite Wallet Package Models.
"""
from decimal import Decimal as _Decimal
from pytsite import odm as _odm, odm_ui as _odm_ui, currency as _currency, auth as _auth, auth_ui as _auth_ui, \
    widget as _widget
from . import _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


_main_currency = _currency.get_main()


class Account(_odm_ui.UIModel):
    """Wallet ODM Model.
    """
    def _setup(self):
        """Hook.
        """
        self._define_field(_odm.field.String('aid', nonempty=True))
        self._define_field(_odm.field.String('currency', nonempty=True))
        self._define_field(_odm.field.String('description'))
        self._define_field(_odm.field.Decimal('balance', round=2))
        self._define_field(_odm.field.Ref('owner', model='user', nonempty=True))
        self._define_field(_odm.field.RefsUniqueList('pending_transactions', model='wallet_transaction'))
        self._define_field(_odm.field.RefsUniqueList('cancelling_transactions', model='wallet_transaction'))
        self._define_field(_odm.field.Dict('options'))

        self._define_index([('aid', _odm.I_ASC)], True)

    @property
    def aid(self) -> str:
        return self.f_get('aid')

    @property
    def currency(self) -> str:
        return self.f_get('currency')

    @property
    def description(self) -> str:
        return self.f_get('description')

    @property
    def balance(self) -> _Decimal:
        return self.f_get('balance')

    @property
    def owner(self) -> _auth.model.User:
        return self.f_get('owner')

    @property
    def pending_transactions(self):
        return self.f_get('pending_transactions')

    @property
    def cancelling_transactions(self):
        return self.f_get('cancelling_transactions')

    @property
    def options(self) -> dict:
        return self.f_get('options')

    def _on_f_set(self, field_name: str, value, **kwargs):
        if field_name == 'currency':
            if value not in _currency.get_all():
                raise _currency.error.CurrencyNotDefined("Currency '{}' is not defined.".format(value))

        return value

    def _pre_delete(self, **kwargs):
        """Hook.

        :param force: only for testing purposes.
        """
        if not kwargs.get('force'):
            f = _odm.find('wallet_transaction').or_where('source', '=', self).or_where('destination', '=', self)
            if f.count():
                raise _odm.error.ForbidEntityDelete('Cannot delete account due to its usage in transaction(s).')

    @classmethod
    def ui_setup_browser(cls, browser):
        """Setup ODM UI browser hook.

        :type browser: pytsite.odm_ui._browser.Browser
        :return: None
        """
        browser.data_fields = ('aid', 'currency', 'balance', 'owner')

    @property
    def ui_browser_data_row(self) -> tuple:
        """Get single UI browser row hook.
        """
        return self.aid, self.currency, str(self.balance), self.owner.full_name

    def ui_setup_m_form(self, form, stage: str):
        """Modify form setup hook.
        :type form: pytsite.form.Base
        """
        if self.is_new:
            form.add_widget(_currency.widget.Select(
                uid='currency',
                weight=10,
                label=self.t('currency'),
                required=True,
                value=self.currency,
            ))
        else:
            form.add_widget(_widget.static.Text(
                uid='currency',
                weight=10,
                label=self.t('currency'),
                title=self.currency,
                value=self.currency,
            ))

        form.add_widget(_widget.input.Text(
            uid='aid',
            weight=20,
            label=self.t('aid'),
            required=True,
            value=self.aid,
        ))
        form.add_rule('aid', _odm.validation.FieldUnique(msg_id='pytsite.wallet@validation_account_id',
                                                         model=self.model, field='aid', exclude_ids=self.id))

        form.add_widget(_auth_ui.widget.UserSelect(
            uid='owner',
            weight=30,
            label=self.t('owner'),
            required=True,
            value=self.owner,
        ))


class Transaction(_odm_ui.UIModel):
    """Transaction ODM Model.
    """
    def _setup(self):
        """Hook.
        """
        self._define_field(_odm.field.Ref('source', model='wallet_account', nonempty=True))
        self._define_field(_odm.field.Ref('destination', model='wallet_account', nonempty=True))
        self._define_field(_odm.field.String('state', default='new'))
        self._define_field(_odm.field.Decimal('amount', round=2))
        self._define_field(_odm.field.String('description'))
        self._define_field(_odm.field.Dict('options'))

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

        return value

    def _pre_delete(self, **kwargs):
        """Hook.
        :param force: only for testing purposes.
        """
        if not kwargs.get('force'):
            raise _odm.error.ForbidEntityDelete('Wallet transactions cannot be deleted.')

    def cancel(self):
        if self.state != 'committed':
            raise _error.ImproperTransactionState('It is possible to cancel only committed transactions.')

        self.f_set('state', 'cancel').save()

        return self

    @classmethod
    def ui_setup_browser(cls, browser):
        """Setup ODM UI browser hook.

        :type browser: pytsite.odm_ui._browser.Browser
        :return: None
        """
        browser.data_fields = ('aid', 'wallet', 'amount')

    @property
    def ui_browser_data_row(self) -> tuple:
        """Get single UI browser row hook.
        """
        return self.description, self.source.aid, 'FIXME'

    @staticmethod
    def ui_is_modification_allowed() -> bool:
        return False

    @staticmethod
    def ui_is_deletion_allowed() -> bool:
        return False
