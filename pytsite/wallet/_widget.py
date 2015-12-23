"""PytSite Wallet Widgets
"""
from pytsite import widget as _w, odm as _odm, auth as _auth, lang as _lang

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class AccountSelect(_w.select.Select):
    """Wallet Account Select Widget
    """
    def __init__(self, uid: str, **kwargs):
        u = _auth.get_current_user()
        items = []

        if u.has_permission('pytsite.odm_ui.browse.wallet_account') or \
                u.has_permission('pytsite.odm_ui.browse_own.wallet_account'):
            f = _odm.find('wallet_account').sort([('aid', _odm.I_ASC)])

            # User can only view its own accounts
            if not u.has_permission('pytsite.odm_ui.browse.wallet_account'):
                f.where('owner', '=', u)

            for acc in f.get():
                label = '{} ({}, {})'.format(acc.description, acc.aid, acc.currency)
                items.append(('wallet_account:' + str(acc.id), label))

        super().__init__(uid, items=items, **kwargs)
