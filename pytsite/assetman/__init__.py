"""Assetman Plugin Init.
"""
# Public API
from ._api import register_package, add, remove, dump_js, dump_css, url, add_inline, dump_inline, get_urls, \
    get_locations, reset, detect_collection

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    """Package init wrapper.
    """
    from pytsite import console, events, lang, tpl
    from . import _console_command, _api

    lang.register_package(__name__)

    # Console commands
    console.register_command(_console_command.Assetman())

    # Events
    events.listen('pytsite.router.dispatch', reset)
    events.listen('pytsite.update.after', lambda: console.run_command('assetman', build=True, no_maintenance=True))

    # Tpl globals
    tpl.register_global('assetman_url', url)
    tpl.register_global('assetman_css', dump_css)
    tpl.register_global('assetman_js', dump_js)
    tpl.register_global('assetman_inline', dump_inline)

__init()
