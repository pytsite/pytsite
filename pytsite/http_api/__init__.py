"""PytSite HTTP API Package.
"""
# Public API
from ._api import handle, url, call

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import router, assetman, events
    from . import _eh

    # HTTP entry point route
    router.add_rule('/api/<int:version>/<path:endpoint>', 'pytsite.http_api@entry')

    # JavaScript helpers
    assetman.register_package(__name__)
    assetman.add('pytsite.http_api@js/common.js', True)

    # Event listeners
    events.listen('pytsite.router.dispatch', _eh.router_dispatch)
    events.listen('pytsite.router.response', _eh.router_response)


_init()
