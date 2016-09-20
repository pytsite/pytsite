"""PytSite Wallet Package.
"""
# Public API
from . import _error as error, _model as model
from . import _field as field, _widget as widget
from ._api import create_account, get_account, create_transaction, commit_transactions_1, commit_transactions_2, \
    cancel_transactions_1, cancel_transactions_2


__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    from pytsite import odm, admin, router, events, assetman, permissions
    from . import _eh

    # Permission group
    permissions.define_group('wallet', 'pytsite.wallet@wallet')

    # ODM models
    odm.register_model('wallet_account', model.Account)
    odm.register_model('wallet_transaction', model.Transaction)

    # Admin sidebar entries
    admin.sidebar.add_section('wallet', 'pytsite.wallet@wallet', 250)
    admin.sidebar.add_menu('wallet', 'accounts', 'pytsite.wallet@accounts',
                           router.ep_path('pytsite.odm_ui@browse', {'model': 'wallet_account'}),
                           'fa fa-credit-card', weight=10, permissions='pytsite.odm_perm.view.wallet_account')
    admin.sidebar.add_menu('wallet', 'transactions', 'pytsite.wallet@transactions',
                           router.ep_path('pytsite.odm_ui@browse', {'model': 'wallet_transaction'}),
                           'fa fa-exchange', weight=20, permissions='pytsite.odm_perm.view.wallet_transaction')

    # Cron event dispatcher
    events.listen('pytsite.cron.1min', _eh.cron_1_min)

    # Admin routes
    abp = admin.base_path()
    router.add_rule(abp + '/odm_ui/wallet_transaction/cancel', 'pytsite.wallet@transactions_cancel')
    router.add_rule(abp + '/odm_ui/wallet_transaction/cancel/submit', 'pytsite.wallet@transactions_cancel_submit')

    assetman.register_package(__name__)

__init()
