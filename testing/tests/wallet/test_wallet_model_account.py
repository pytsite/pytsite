"""PytSite Wallet Account Tests.
"""
import pytest
import decimal
from pytsite import auth, wallet, currency, odm, db

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class TestWalletModelAccount:
    user = None
    """:type: auth.model.User"""

    @classmethod
    def setup_class(cls):
        db.get_collection('users').drop()
        db.get_collection('wallet_accounts').drop()
        db.get_collection('wallet_transactions').drop()

        cls.user = auth.create_user('test@test.com').save()

    @classmethod
    def teardown_class(cls):
        pass

    def test_init(self):
        acc = wallet.create_account('acc', currency.get_main(), TestWalletModelAccount.user, 'Some description', 12.34)
        assert isinstance(acc, wallet.model.Account)
        assert not acc.is_new
        assert acc.model == 'wallet_account'
        assert acc.aid == 'acc'
        assert acc.currency == currency.get_main()
        assert acc.description == 'Some description'
        assert acc.balance == decimal.Decimal('12.34')
        assert acc.owner == TestWalletModelAccount.user
        assert acc.pending_transactions == ()
        assert acc.cancelling_transactions == ()
        assert acc.options == {}

        # Cleanup
        acc.delete(force=True)

    def test_on_f_set(self):
        acc = wallet.create_account('acc', currency.get_main(), TestWalletModelAccount.user)

        with pytest.raises(currency.error.CurrencyNotDefined):
            acc.f_set('currency', 'unknown')

        # Cleanup
        acc.delete(force=True)

    def test_pre_delete(self):
        acc1 = wallet.create_account('acc1', currency.get_main(), TestWalletModelAccount.user)
        acc2 = wallet.create_account('acc2', currency.get_main(), TestWalletModelAccount.user)
        t = wallet.create_transaction(acc1, acc2, 1)

        with pytest.raises(odm.error.ForbidEntityDelete):
            acc1.delete()

        t.delete(force=True)
        acc1.delete()

        # Cleanup
        acc2.delete(force=True)
