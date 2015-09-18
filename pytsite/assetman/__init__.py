"""Assetman Plugin Init.
"""
# Public API
from ._functions import register_package, add, remove, dump_js, dump_css, get_url

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    """Package init wrapper.
    """
    from pytsite import console, events, lang
    from . import _commands, _functions

    def app_update_event():
        from pytsite import console
        console.run_command('assetman:build')

    lang.register_package(__name__)

    # Console commands
    console.register_command(_commands.CompileAssets())

    # Events
    events.listen('pytsite.router.dispatch', _functions.reset)
    events.listen('pytsite.update.after', app_update_event)

__init()
