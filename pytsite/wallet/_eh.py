"""PytSite Wallet Event Handlers.
"""
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def cron_1_min():
    _api.commit_transactions_1()
    _api.commit_transactions_2()
    _api.cancel_transactions_1()
    _api.cancel_transactions_2()
