"""PytSite Setup Package.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import console as _console, lang as _lang
from . import _command

# Initializing Update module
__import__('pytsite.update')

_lang.register_package(__name__)
_console.register_command(_command.Setup())


# Public API
from ._function import *
