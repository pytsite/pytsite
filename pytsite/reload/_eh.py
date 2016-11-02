"""PytSite Reload Event Handlers.
"""
from pytsite import router as _router, lang as _lang, auth as _auth, assetman as _assetman
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def router_dispatch():
    if _api.get_flag() and _auth.get_current_user().has_permission('pytsite.reload.reload'):
        _assetman.add('pytsite.reload@js/reload.js')
        _router.session().add_warning_message(_lang.t(_api.RELOAD_MSG_ID))
