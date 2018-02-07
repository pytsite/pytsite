"""PytSite pip Support
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

# Public API
from . import _error as error
from ._api import get_installed_info, get_installed_version, is_installed, install, uninstall

# Console commands
from pytsite import lang as _lang, console as _console
from . import _console_commands
_lang.register_package(__name__)
_console.register_command(_console_commands.Install())
_console.register_command(_console_commands.Uninstall())
