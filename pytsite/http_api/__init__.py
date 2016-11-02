"""PytSite HTTP API Package.
"""
# Public API
from ._api import register_handler, call_endpoint, get, post, patch, delete, url

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import router, assetman, events
    from . import _eh

    router.add_rule('/api/<int:version>/<path:endpoint>', 'pytsite.http_api@entry')

    assetman.register_package(__name__)
    assetman.add('pytsite.http_api@js/common.js', True)

    events.listen('pytsite.router.dispatch', _eh.router_dispatch)
    events.listen('pytsite.router.response', _eh.router_response)


_init()
