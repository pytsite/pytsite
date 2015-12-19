"""PytSite Wallet Transaction Tests.
"""
import pytest
import decimal
from datetime import datetime
from pytsite import wallet, currency, auth, odm, db

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class TestWalletModelTransaction:
    user = None
    """:type: auth.model.User"""

    acc1 = None
    """:type: wallet.model.Account"""

    acc2 = None
    """:type: wallet.model.Account"""

    @classmethod
    def setup_class(cls):
        db.get_collection('users').drop()
        db.get_collection('wallet_accounts').drop()
        db.get_collection('wallet_transactions').drop()

        cls.user = auth.create_user('test@test.com').save()
        cls.acc1 = wallet.create_account('acc1', currency.get_main(), cls.user)
        cls.acc2 = wallet.create_account('acc2', currency.get_main(), cls.user)

    @classmethod
    def teardown_class(cls):
        pass

    def test_init(self):
        now = datetime.now()

        t = wallet.create_transaction(self.acc1, self.acc2, 12.34, now, 'Some description')

        assert not t.is_new
        assert t.time == now
        assert t.source == self.acc1
        assert t.destination == self.acc2
        assert t.state == 'new'
        assert t.amount == decimal.Decimal('12.34')
        assert t.description == 'Some description'
        assert t.exchange_rate == decimal.Decimal(1)
        assert t.options == {}

        # Cleanup
        t.delete(force=True)

    def test_on_f_set(self):
        t = wallet.create_transaction(self.acc1, self.acc2, 12.34)

        with pytest.raises(ValueError):
            t.f_set('source', self.acc2)

        with pytest.raises(ValueError):
            t.f_set('destination', self.acc1)

        with pytest.raises(ValueError):
            t.f_set('amount', 34.21)

        t.f_set('description', 'Another description')
        t.f_set('options', {'a': 'b'})

        # Cleanup
        t.delete(force=True)

    def test_pre_delete(self):
        t = wallet.create_transaction(self.acc1, self.acc2, 12.34)

        with pytest.raises(odm.error.ForbidEntityDelete):
            t.delete()

        # Cleanup
        t.delete(force=True)
