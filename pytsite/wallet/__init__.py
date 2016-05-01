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
    from pytsite import odm, admin, router, events, assetman, permission
    from . import _eh

    # ODM models
    odm.register_model('wallet_account', model.Account)
    odm.register_model('wallet_transaction', model.Transaction)

    # Permissions
    permission.define_permission('pytsite.odm_ui.cancel.wallet_transaction',
                                 'pytsite.wallet@odm_ui_permission_cancel_wallet_transaction',
                                 'pytsite.wallet')

    # Admin sidebar entries
    admin.sidebar.add_section('wallet', 'pytsite.wallet@wallet', 250)
    admin.sidebar.add_menu('wallet', 'accounts', 'pytsite.wallet@accounts',
                           router.ep_url('pytsite.odm_ui.ep.browse', {'model': 'wallet_account'}),
                           'fa fa-credit-card', weight=10, permissions='pytsite.odm_ui.browse.wallet_transaction')
    admin.sidebar.add_menu('wallet', 'transactions', 'pytsite.wallet@transactions',
                           router.ep_url('pytsite.odm_ui.ep.browse', {'model': 'wallet_transaction'}),
                           'fa fa-exchange', weight=20, permissions='pytsite.odm_ui.browse.wallet_transaction')

    # Cron event dispatcher
    events.listen('pytsite.cron.1min', _eh.cron_1_min)

    # Admin routes
    router.add_rule(admin.base_path() + '/odm_ui/wallet_transaction/cancel', 'pytsite.wallet.ep.transactions_cancel',
                    filters='pytsite.auth.ep.filter_authorize:permissions=pytsite.odm_ui.delete.wallet_transaction')
    router.add_rule(admin.base_path() + '/odm_ui/wallet_transaction/cancel/submit',
                    'pytsite.wallet.ep.transactions_cancel_submit',
                    filters='pytsite.auth.ep.filter_authorize:permissions=pytsite.odm_ui.delete.wallet_transaction')

    assetman.register_package(__name__)

__init()
