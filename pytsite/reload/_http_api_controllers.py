"""PytSite Reload HTTP API.
"""
from pytsite import auth as _auth, routing as _routing
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class PostReload(_routing.Controller):
    def exec(self) -> dict:
        if not _auth.get_current_user().has_permission('pytsite.reload'):
            raise self.forbidden()

        _api.reload()

        return {'status': True}
