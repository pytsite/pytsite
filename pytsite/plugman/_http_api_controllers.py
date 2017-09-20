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

        plugin_name = self.arg('name')

        _api.install(plugin_name)

        return _api.plugin_info(plugin_name)


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

        _api.install(self.arg('name'))
        _reload.reload()

        return {'status': True}
