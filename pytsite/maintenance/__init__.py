"""PytSite Maintenance Package.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

# Public API
from ._api import enable, disable, is_enabled


def _init():
    from pytsite import console, lang
    from . import _console_command

    lang.register_package(__name__)
    console.register_command(_console_command.Maintenance())


_init()
