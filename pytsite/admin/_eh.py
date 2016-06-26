"""
"""
from pytsite import lang as _lang, auth as _auth, router as _router, hreflang as _hreflang, http as _http
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def router_dispatch():
    if _router.current_path(True).startswith(_api.base_path()):
        # Check permissions ONLY for GET-requests
        if _router.request().method == 'GET' and not _auth.current_user().has_permission('pytsite.admin.use'):
            raise _http.error.Forbidden()

        # Alternate languages
        for lng in _lang.langs(False):
            _hreflang.add(lng, _router.url(_router.current_path(), lang=lng))
