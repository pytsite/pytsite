"""PytSite Maintenance Module.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import console as _console, lang as _lang
from . import _command

_lang.register_package(__name__)
_console.register_command(_command.Maintenance())


# Public API
from ._function import enable, disable, is_enabled
