"""PytSite Reload Package
"""
# Public API
from ._api import RELOAD_MSG_ID, reload, on_before_reload, on_reload, set_flag, get_flag

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import lang, console
    from . import _console_command

    lang.register_package(__name__)
    console.register_command(_console_command.Reload())


_init()
