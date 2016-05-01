"""PytSite Wallet Endpoints
"""
from pytsite import http as _http, router as _router, odm as _odm, lang as _lang, metatag as _metatag, admin as _admin
from . import _forms, _model

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def transactions_cancel(args: dict, inp: dict):
    browse_url = _router.ep_url('pytsite.odm_ui.ep.browse', {'model': 'wallet_transaction'})

    ids = inp.get('ids')
    if not ids:
        return _http.response.Redirect(browse_url)

    if isinstance(ids, str):
        ids = (ids,)

    frm = _forms.TransactionsCancel('odm-ui-d-form', model='wallet_transaction', eids=ids)

    return _admin.render_form(frm)


def transactions_cancel_submit(args: dict, inp: dict):
    ids = inp.get('ids')
    if not ids:
        return _http.response.Redirect(inp.get('__redirect'))

    if isinstance(ids, str):
        ids = (ids,)

    for eid in ids:
        entity = _odm.dispense('wallet_transaction', eid)  # type: _model.Transaction
        entity.cancel()

    redirect = inp.get('__redirect', _router.ep_url('pytsite.odm_ui.ep.browse', {'model': 'wallet_transaction'}))

    return _http.response.Redirect(redirect)
