"""PytSite Wallet API Functions.
"""
from pytsite import odm as _odm, auth as _auth
from . import _error
from ._model import Account as _Account, Transaction as _Transaction


__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def create_account(aid: str, currency: str, owner: _auth.model.User, description: str=None, balance=0.0) -> _Account:
    """Create new account.
    :type balance: int | float | str | decimal.Decimal
    """
    try:
        get_account(aid)
        raise _error.AccountExists("Account '{}' is already exists.".format(aid))
    except _error.AccountNotExists:
        pass

    acc = _odm.dispense('wallet_account')

    acc.f_set('aid', aid)
    acc.f_set('currency', currency)
    acc.f_set('owner', owner)
    acc.f_set('description', description)
    acc.f_set('balance', balance)
    acc.save()

    return acc


def get_account(aid: str) -> _Account:
    """Find account by title.
    """
    acc = _odm.find('wallet_account').where('aid', '=', aid).first()
    if not acc:
        raise _error.AccountNotExists("Account with id '{}' is not exists.".format(aid))

    return acc


def create_transaction(src: _Account, dst: _Account, amount, description: str=None) -> _Transaction:
    """Create transaction.

    :type amount: int | float | str | decimal.Decimal
    """
    t = _odm.dispense('wallet_transaction')
    t.f_set('source', src)
    t.f_set('destination', dst)
    t.f_set('amount', amount)
    t.f_set('description', description)
    t.save()

    return t


def commit_transactions_1():
    """Commit transactions, step one. Change state from 'new' to 'pending'.
    """
    for t in _odm.find('wallet_transaction').where('state', '=', 'new').get():
        src = t.source
        """:type: _Account"""
        if t not in src.f_get('pending_transactions'):
            src.f_sub('balance', t.amount).f_add('pending_transactions', t).save()

        dst = t.destination
        """:type: _Account"""
        if t not in dst.f_get('pending_transactions'):
            dst.f_add('balance', t.amount).f_add('pending_transactions', t).save()

        t.f_set('state', 'pending').save()


def commit_transactions_2():
    """Commit transactions, step two. Change state from 'pending' to 'committed'.
    """
    for t in _odm.find('wallet_transaction').where('state', '=', 'pending').get():
        src = t.source
        """:type: _Account"""
        if t in src.f_get('pending_transactions'):
            src.f_sub('pending_transactions', t).save()

        dst = t.destination
        """:type: _Account"""
        if t in dst.f_get('pending_transactions'):
            dst.f_sub('pending_transactions', t).save()

        t.f_set('state', 'committed').save()


def cancel_transactions_1():
    """Cancelling transactions, step one. Change state from 'cancel' to 'cancelling'.
    """
    for t in _odm.find('wallet_transaction').where('state', '=', 'cancel').get():
        src = t.source
        """:type: _Account"""
        if t not in src.f_get('cancelling_transactions'):
            src.f_add('balance', t.amount).f_add('cancelling_transactions', t).save()

        dst = t.destination
        """:type: _Account"""
        if t not in dst.f_get('cancelling_transactions'):
            dst.f_sub('balance', t.amount).f_add('cancelling_transactions', t).save()

        t.f_set('state', 'cancelling').save()


def cancel_transactions_2():
    """Cancelling transactions, step two. Change state from 'cancelling' to 'cancelled'.
    """
    for t in _odm.find('wallet_transaction').where('state', '=', 'cancelling').get():
        src = t.source
        """:type: _Account"""
        if t in src.f_get('cancelling_transactions'):
            src.f_sub('cancelling_transactions', t).save()

        dst = t.destination
        """:type: _Account"""
        if t in dst.f_get('cancelling_transactions'):
            dst.f_sub('cancelling_transactions', t).save()

        t.f_set('state', 'cancelled').save()
