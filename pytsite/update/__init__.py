"""PytSite Update
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

# Public API
from ._api import on_update_stage_1, on_update_stage_2, on_update, on_update_after


def _init():
    """Init wrapper
    """
    from pytsite import console, lang
    from . import _console_command

    lang.register_package(__name__)
    console.register_command(_console_command.Update())


_init()
