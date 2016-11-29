"""PytSite Plugman HTTP API.
"""
from pytsite import auth as _auth, http as _http, reload as _reload
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _check_args(**kwargs):
    if not _auth.get_current_user().has_permission('pytsite.plugman.manage'):
        raise _http.error.Forbidden('Insufficient permissions')

    if not kwargs.get('name'):
        raise _http.error.InternalServerError('Plugin name is not specified')

    return kwargs


def post_install(**kwargs) -> dict:
    info = _api.install(_check_args(**kwargs).get('name'))

    return info


def post_uninstall(**kwargs) -> dict:
    _api.uninstall(_check_args(**kwargs).get('name'))
    _reload.reload(False)

    return {'status': True}


def post_upgrade(**kwargs) -> dict:
    info = _api.upgrade(_check_args(**kwargs).get('name'))
    _reload.reload(False)

    return info
