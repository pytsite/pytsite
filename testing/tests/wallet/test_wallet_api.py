"""PytSite Wallet API Tests.
"""
import pytest
import decimal as _decimal
from pytsite import wallet, currency, auth, db

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class TestApi:
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

    def test_create_account(self):
        # Normal
        acc = wallet.create_account('acc', currency.get_main(), TestApi.user)

        # Duplicate
        with pytest.raises(wallet.error.AccountExists):
            wallet.create_account('acc', currency.get_main(), TestApi.user)

        acc.delete()

        # Bad currency
        with pytest.raises(currency.error.CurrencyNotDefined):
            wallet.create_account('acc', 'abc', TestApi.user)

    def test_get_account(self):
        acc = wallet.create_account('acc', currency.get_main(), TestApi.user)
        assert wallet.get_account('acc') is acc
        acc.delete()

        with pytest.raises(wallet.error.AccountNotExists):
            wallet.get_account('acc')

    def test_create_transaction(self):
        acc1 = wallet.create_account('acc1', currency.get_main(), TestApi.user)
        acc2 = wallet.create_account('acc2', currency.get_main(), TestApi.user)

        t = wallet.create_transaction(acc1, acc2, 123.45)
        t.delete(force=True)

        acc1.delete(force=True)
        acc2.delete(force=True)

    def test_commit_transactions(self):
        acc1 = wallet.create_account('acc1', currency.get_main(), TestApi.user)
        acc2 = wallet.create_account('acc2', currency.get_main(), TestApi.user)
        t = wallet.create_transaction(acc1, acc2, 123.45)

        assert t.state == 'new'
        assert acc1.pending_transactions == ()
        assert acc2.pending_transactions == ()

        wallet.commit_transactions_1()
        assert t.state == 'pending'
        assert acc1.balance == _decimal.Decimal('-123.45')
        assert acc2.balance == _decimal.Decimal('123.45')
        assert acc1.pending_transactions == (t,)
        assert acc2.pending_transactions == (t,)

        wallet.commit_transactions_2()
        assert t.state == 'committed'
        assert acc1.balance == _decimal.Decimal('-123.45')
        assert acc2.balance == _decimal.Decimal('123.45')
        assert acc1.pending_transactions == ()
        assert acc2.pending_transactions == ()

        t.delete(force=True)
        acc1.delete(force=True)
        acc2.delete(force=True)

    def test_cancel_transactions(self):
        acc1 = wallet.create_account('acc1', currency.get_main(), TestApi.user)
        acc2 = wallet.create_account('acc2', currency.get_main(), TestApi.user)
        t = wallet.create_transaction(acc1, acc2, 123.45)

        wallet.commit_transactions_1()
        wallet.commit_transactions_2()

        t.cancel()
        assert t.state == 'cancel'

        wallet.cancel_transactions_1()
        assert t.state == 'cancelling'
        assert acc1.balance == _decimal.Decimal(0)
        assert acc2.balance == _decimal.Decimal(0)
        assert acc1.cancelling_transactions == (t,)
        assert acc2.cancelling_transactions == (t,)

        wallet.cancel_transactions_2()
        assert t.state == 'cancelled'
        assert acc1.balance == _decimal.Decimal(0)
        assert acc2.balance == _decimal.Decimal(0)
        assert acc1.cancelling_transactions == ()
        assert acc2.cancelling_transactions == ()

        t.delete(force=True)
        acc1.delete(force=True)
        acc2.delete(force=True)
