"""PytSite Wallet Forms
"""
from pytsite import odm_ui as _odm_ui, router as _router, metatag as _metatag, lang as _lang, http as _http

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class TransactionsCancel(_odm_ui.forms.MassAction):
    """Transactions Cancel Form.
    """
    def _setup_form(self):
        """Hook.
        """
        super()._setup_form()

        # Check permissions
        if not _odm_ui.check_permissions('cancel', self._model, self._eids):
            raise _http.error.Forbidden()

        # Action URL
        self._action = _router.ep_url('pytsite.wallet.ep.transactions_cancel_submit')

        # Page title
        _metatag.t_set('title', _lang.t('pytsite.wallet@odm_ui_form_title_cancel_' + self._model))

    def _setup_widgets(self):
        """Hook.
        """
        super()._setup_widgets()

        # Change submit button color
        self.get_widget('action-submit').color = 'danger'
