"""Assetman Plugin Init
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _app_update_event():
    from pytsite.core import console
    console.run_command('assetman:build')


def __init():
    from pytsite.core import console, events
    from . import _commands

    # Console commands
    console.register_command(_commands.BuildAssets())

    # Events
    events.listen('app.update', _app_update_event)

__init()


# Public API
from ._functions import register_package, add, add_js, add_css, dump_js, dump_css
