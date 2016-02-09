"""PytSite Setup Package.
"""
from pytsite import console as _console, lang as _lang
from . import _console_command

# Public API
from ._api import is_setup_completed

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


# Initializing Update module
__import__('pytsite.update')

_lang.register_package(__name__)
_console.register_command(_console_command.Setup())
