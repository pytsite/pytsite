"""Assetman Plugin Init.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'





def __init():
    from pytsite.core import console, events
    from . import _commands, _functions

    def app_update_event():
        from pytsite.core import console
        console.run_command('assetman:build')

    # Console commands
    console.register_command(_commands.BuildAssets())

    # Events
    events.listen('pytsite.core.router.dispatch', _functions.reset)
    events.listen('app.update', app_update_event)

__init()


# Public API
from ._functions import register_package, add, remove, dump_js, dump_css, get_url
