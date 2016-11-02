"""PytSite Reload Package.
"""
# Public API
from ._api import reload, set_flag, get_flag

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import lang, console, permissions, http_api, events, assetman
    from . import _console_command, _eh

    lang.register_package(__name__)
    console.register_command(_console_command.Reload())
    assetman.register_package(__name__)
    permissions.define_permission('pytsite.reload.reload', 'pytsite.reload@reload_application_permission', 'app')
    http_api.register_handler('reload', 'pytsite.reload.http_api')
    events.listen('pytsite.router.dispatch', _eh.router_dispatch)


_init()
