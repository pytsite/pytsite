"""PytSite Reload Package
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

# Public API
from ._api import RELOAD_MSG_ID, reload, on_before_reload, on_reload, set_flag, get_flag


def _init():
    from pytsite import lang, console
    from . import _console_command

    lang.register_package(__name__)
    console.register_command(_console_command.Reload())


_init()
