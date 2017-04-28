"""PytSite Reload Package.
"""
# Public API
from ._api import reload, set_flag, get_flag

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import lang, console, permissions, http_api, router, assetman
    from . import _console_command, _eh, _http_api

    lang.register_package(__name__)
    console.register_command(_console_command.Reload())

    assetman.register_package(__name__)
    assetman.t_js(__name__ + '@**/*.js')

    permissions.define_permission('pytsite.reload', 'pytsite.reload@reload_application_permission', 'app')

    http_api.handle('POST', 'reload', _http_api.reload, 'pytsite.reload@reload')

    router.on_dispatch(_eh.router_dispatch)


_init()
