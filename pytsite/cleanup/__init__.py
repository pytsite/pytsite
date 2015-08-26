"""PytSite Cleanup Module.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import console as _console
from . import _command


_console.register_command(_command.Cleanup())
_console.register_command(_command.CleanupOldSessions())
_console.register_command(_command.CleanupTmpFiles())
