"""PytSite Update Package.
"""
from pytsite import console as _console, lang as _lang
from . import _console_command

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_lang.register_package(__name__)
_console.register_command(_console_command.Update())
