"""Console Plugin Init.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    from . import _functions, _command
    _functions.register_command(_command.Cleanup())
    _functions.register_command(_command.CleanupOldSessions())
    _functions.register_command(_command.CleanupTmpFiles())
    _functions.register_command(_command.Setup())
    _functions.register_command(_command.Cron())

__init()

# Public API
from ._functions import Abstract as AbstractConsoleCommand, register_command, run, run_console_command, \
    print_info, print_success, print_error, print_warning
from . import _error as error
