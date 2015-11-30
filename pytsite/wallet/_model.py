"""PytSite Wallet Package Models.
"""
from pytsite import odm as _odm, odm_ui as _odm_ui, currency as _currency, auth as _auth, auth_ui as _auth_ui, \
    widget as _widget

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


_main_currency = _currency.get_main()


class Wallet(_odm_ui.Model):
    """Wallet ODM Model.
    """
    def _setup(self):
        """Hook.
        """
        self._define_field(_odm.field.String('currency', nonempty=True))
        self._define_field(_odm.field.String('title', nonempty=True))
        self._define_field(_odm.field.String('description'))
        self._define_field(_currency.field.Currency('balance'))
        self._define_field(_odm.field.Ref('owner', model='user', nonempty=True))
        self._define_field(_odm.field.Dict('options'))

    @property
    def currency(self) -> str:
        return self.f_get('currency')

    @property
    def title(self) -> str:
        return self.f_get('title')

    @property
    def description(self) -> str:
        return self.f_get('description')

    @property
    def balance(self) -> _currency.field.Currency:
        return self.f_get('balance')

    @property
    def owner(self) -> _auth.model.User:
        return self.f_get('owner')

    @property
    def options(self) -> dict:
        return self.f_get('options')

    def setup_browser(self, browser):
        """Setup ODM UI browser hook.

        :type browser: pytsite.odm_ui._browser.Browser
        :return: None
        """
        browser.data_fields = ('title', 'currency', 'balance', 'owner')

    def get_browser_data_row(self) -> tuple:
        """Get single UI browser row hook.
        """
        return self.title, self.currency, 'FIXME', self.owner.full_name

    def setup_m_form(self, form, stage: str):
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
            uid='title',
            weight=20,
            label=self.t('title'),
            required=True,
            value=self.title,
        ))

        form.add_widget(_auth_ui.widget.UserSelect(
            uid='owner',
            weight=30,
            label=self.t('owner'),
            required=True,
            value=self.owner,
        ))


class Transaction(_odm_ui.Model):
    """Transaction ODM Model.
    """
    def _setup(self):
        """Hook.
        """
        self._define_field(_odm.field.String('title', nonempty=True))
        self._define_field(_odm.field.String('description'))
        self._define_field(_odm.field.Ref('wallet', model='wallet', nonempty=True))
        self._define_field(_currency.field.Currency('amount'))
        self._define_field(_odm.field.Dict('options'))

    @property
    def title(self) -> str:
        return self.f_get('title')

    @property
    def description(self) -> str:
        return self.f_get('description')

    @property
    def wallet(self) -> Wallet:
        return self.f_get('wallet')

    @property
    def amount(self) -> _currency.field.Currency:
        return self.f_get('amount')

    @property
    def options(self) -> dict:
        return self.f_get('options')

    def setup_browser(self, browser):
        """Setup ODM UI browser hook.

        :type browser: pytsite.odm_ui._browser.Browser
        :return: None
        """
        browser.data_fields = ('title', 'wallet', 'amount')

    def get_browser_data_row(self) -> tuple:
        """Get single UI browser row hook.
        """
        return self.title, self.wallet.title, 'FIXME'
