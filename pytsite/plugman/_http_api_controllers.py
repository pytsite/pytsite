"""PytSite Plugman HTTP API.
"""
from pytsite import routing as _routing, auth as _auth, reload as _reload
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class PostInstall(_routing.Controller):
    def exec(self) -> dict:
        if not _auth.get_current_user().has_permission('pytsite.plugman.manage'):
            raise self.forbidden()

        info = _api.install(self.arg('name'))

        return info


class PostUninstall(_routing.Controller):
    def exec(self) -> dict:
        if not _auth.get_current_user().has_permission('pytsite.plugman.manage'):
            raise self.forbidden()

        _api.uninstall(self.arg('name'))
        _reload.reload()

        return {'status': True}


class PostUpgrade(_routing.Controller):
    def exec(self) -> dict:
        if not _auth.get_current_user().has_permission('pytsite.plugman.manage'):
            raise self.forbidden()

        info = _api.upgrade(self.arg('name'))
        _reload.reload()

        return info
