"""jQuery UI.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core import assetman, events


def dispatch_event_handler():
    assetman.add_css('pytsite.jquery_ui@jquery-ui.min.css')
    assetman.add_js('pytsite.jquery_ui@jquery-ui.min.js')


assetman.register_package(__name__)

events.listen('pytsite.core.router.dispatch', dispatch_event_handler)
