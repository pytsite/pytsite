"""Assetman Plugin Init.
"""
# Public API
from ._functions import register_package, add, remove, dump_js, dump_css, url, add_inline, dump_inline

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    """Package init wrapper.
    """
    from pytsite import console, events, lang, tpl
    from . import _console_command, _functions

    lang.register_package(__name__)

    # Console commands
    console.register_command(_console_command.Assetman())

    # Events
    events.listen('pytsite.router.dispatch', _functions.reset)
    events.listen('pytsite.update.after', lambda: console.run_command('assetman', build=True, no_maintenance=True))

    tpl.register_global('asset_url', url)
    tpl.register_global('assetman_add', add)
    tpl.register_global('assetman_css', dump_css)
    tpl.register_global('assetman_js', dump_js)
    tpl.register_global('assetman_inline', dump_inline)

__init()
