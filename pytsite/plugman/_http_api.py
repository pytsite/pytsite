"""PytSite Plugman HTTP API.
"""
from pytsite import auth as _auth, http as _http, reload as _reload
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _check_permissions():
    if not _auth.get_current_user().has_permission('pytsite.plugman.manage'):
        raise _http.error.Forbidden('Insufficient permissions')


def post_install(inp: dict, name: str) -> dict:
    _check_permissions()
    info = _api.install(name)

    return info


def post_uninstall(inp: dict, name: str) -> dict:
    _check_permissions()
    _api.uninstall(name)
    _reload.reload()

    return {'status': True}


def post_upgrade(inp: dict, name: str) -> dict:
    _check_permissions()
    info = _api.upgrade(name)
    _reload.reload()

    return info
