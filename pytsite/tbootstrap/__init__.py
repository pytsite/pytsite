"""Twitter Bootstrap Init
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core import events, assetman


def dispatch_event_handler():
    assetman.add_css(__name__ + '@bootstrap/css/bootstrap.min.css')
    assetman.add_css(__name__ + '@font-awesome/css/font-awesome.min.css')
    assetman.add_js(__name__ + '@bootstrap/js/bootstrap.min.js')

assetman.register_package(__name__)
events.listen('router.dispatch', dispatch_event_handler)
