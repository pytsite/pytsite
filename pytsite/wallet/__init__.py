"""PytSite Wallet Package Init.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    from pytsite import odm, admin, router
    from . import _model

    odm.register_model('wallet', _model.Wallet)
    odm.register_model('wallet_transaction', _model.Transaction)

    admin.sidebar.add_section('wallet', 'pytsite.wallet@wallet', 250)
    admin.sidebar.add_menu('wallet', 'wallets', 'pytsite.wallet@wallets',
                           router.ep_url('pytsite.odm_ui.ep.browse', {'model': 'wallet'}),
                           'fa fa-credit-card', weight=10, permissions='pytsite.odm_ui.browse.wallet_transaction')
    admin.sidebar.add_menu('wallet', 'transactions', 'pytsite.wallet@transactions',
                           router.ep_url('pytsite.odm_ui.ep.browse', {'model': 'wallet_transaction'}),
                           'fa fa-exchange', weight=20, permissions='pytsite.odm_ui.browse.wallet_transaction')

__init()
