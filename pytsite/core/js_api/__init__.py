"""JS API.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core import events, router, assetman


def dispatch_event_handler():
    assetman.add_js(__name__ + '@js/js_api.js')

assetman.register_package(__name__)
events.listen('router.dispatch', dispatch_event_handler)

router.add_rule('/core/js_api/<string:ep>', 'pytsite.core.js_api.eps.request', methods=('GET', 'POST'))
