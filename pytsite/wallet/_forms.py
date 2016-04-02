"""PytSite Wallet Forms
"""
from pytsite import odm_ui as _odm_ui, router as _router, metatag as _metatag, lang as _lang

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class TransactionsCancel(_odm_ui.forms.Delete):
    """Transactions Cancel Form.
    """
    def setup(self):
        """Hook.
        """
        super().setup()

        # Action URL
        self._action = _router.ep_url('pytsite.wallet.ep.transactions_cancel_submit')

        # Page title
        _metatag.t_set('title', _lang.t('pytsite.wallet@odm_ui_form_title_delete_wallet_transaction'))
