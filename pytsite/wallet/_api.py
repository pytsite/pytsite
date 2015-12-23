"""PytSite Wallet API Functions.
"""
from typing import Iterable as _Iterable
from datetime import datetime as _datetime
from pytsite import odm as _odm, auth as _auth
from . import _error
from ._model import Account as _Account, Transaction as _Transaction

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def create_account(aid: str, currency: str, owner: _auth.model.User, description: str, balance=0.0) -> _Account:
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


def create_transaction(src: _Account, dst: _Account, amount, date_time: _datetime=None,
                       description: str=None) -> _Transaction:
    """Create transaction.

    :type amount: int | float | str | decimal.Decimal
    """
    t = _odm.dispense('wallet_transaction')
    """:type: _Transaction"""

    t.f_set('source', src)
    t.f_set('destination', dst)
    t.f_set('amount', amount)
    t.f_set('description', description)

    if date_time:
        t.f_set('time', date_time)

    t.save()

    return t


def get_transactions(state: str=None, from_dt: _datetime=None, to_dt: _datetime=None) -> _Iterable[_Transaction]:
    """Find transactions.
    """
    f = _odm.find('wallet_transaction')
    f.sort([('time', _odm.I_DESC)])

    if state:
        f.where('state', '=', state)
    if from_dt:
        f.where('time', '>=', from_dt)
    if to_dt:
        f.where('time', '<=', to_dt)

    return f.get()


def commit_transactions_1():
    """Commit transactions, step one. Change state from 'new' to 'pending'.
    """
    for t in get_transactions('new'):
        # Decrease source account
        src = t.source
        """:type: _Account"""

        dst = t.destination
        """:type: _Account"""

        if src != dst:
            if t not in src.pending_transactions:
                src.f_sub('balance', t.amount)
                src.f_add('pending_transactions', t)
                src.save()

            # Increase destination account
            if t not in dst.pending_transactions:
                dst.f_add('balance', t.amount * t.exchange_rate)
                dst.f_add('pending_transactions', t)
                dst.save()

        t.f_set('state', 'pending').save()


def commit_transactions_2():
    """Commit transactions, step two. Change state from 'pending' to 'committed'.
    """
    for t in get_transactions('pending'):
        src = t.source
        """:type: _Account"""

        dst = t.destination
        """:type: _Account"""

        if src != dst:
            if t in src.pending_transactions:
                src.f_sub('pending_transactions', t).save()

            if t in dst.pending_transactions:
                dst.f_sub('pending_transactions', t).save()

        t.f_set('state', 'committed').save()


def cancel_transactions_1():
    """Cancelling transactions, step one. Change state from 'cancel' to 'cancelling'.
    """
    for t in get_transactions('cancel'):
        src = t.source
        """:type: _Account"""

        dst = t.destination
        """:type: _Account"""

        if src != dst:
            # Increase source account
            if t not in src.cancelling_transactions:
                src.f_add('balance', t.amount)
                src.f_add('cancelling_transactions', t)
                src.save()

            # Decrease destination account
            if t not in dst.cancelling_transactions:
                dst.f_sub('balance', t.amount * t.exchange_rate)
                dst.f_add('cancelling_transactions', t)
                dst.save()

        t.f_set('state', 'cancelling').save()


def cancel_transactions_2():
    """Cancelling transactions, step two. Change state from 'cancelling' to 'cancelled'.
    """
    for t in get_transactions('cancelling'):
        src = t.source
        """:type: _Account"""

        dst = t.destination
        """:type: _Account"""

        if src != dst:
            if t in src.f_get('cancelling_transactions'):
                src.f_sub('cancelling_transactions', t).save()

            if t in dst.f_get('cancelling_transactions'):
                dst.f_sub('cancelling_transactions', t).save()

        t.f_set('state', 'cancelled').save()
