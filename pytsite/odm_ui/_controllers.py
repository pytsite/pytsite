"""ODM UI Endpoints.
"""
from pytsite import tpl as _tpl, odm as _odm, admin as _admin, assetman as _assetman, router as _router, \
    routing as _routing
from . import _api, _browser

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Browse(_routing.Controller):
    def exec(self) -> str:
        _assetman.preload('pytsite.odm_ui@js/odm-ui-browser.js')

        return _admin.render(_tpl.render('pytsite.odm_ui@browser', {
            'table': _browser.Browser(self.arg('model')).render()
        }))


class ModifyForm(_routing.Controller):
    def exec(self) -> str:
        """Get entity create/modify form.
        """
        model = self.arg('model')
        eid = self.arg('eid')
        try:
            frm = _api.get_m_form(model, eid if eid != '0' else None)
            return _admin.render_form(frm)

        except _odm.error.EntityNotFound:
            raise self.not_found()


class DeleteForm(_routing.Controller):
    def exec(self) -> str:
        model = self.arg('model')

        # Entities IDs to delete
        ids = _router.request().inp.get('ids', [])
        if isinstance(ids, str):
            ids = [ids]

        # No required arguments has been received
        if not model or not ids:
            raise self.not_found()

        return _admin.render_form(_api.get_d_form(model, ids))
