"""Console Plugin Init.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from . import _commands
from ._functions import Abstract as AbstractConsoleCommand, register_command, run, run_console_command, \
    print_info, print_success, print_error, print_warning

# Builtin commands
register_command(_commands.Cleanup())
register_command(_commands.CleanupOldSessions())
register_command(_commands.CleanupTmpFiles())
register_command(_commands.Setup())
register_command(_commands.Cron())
