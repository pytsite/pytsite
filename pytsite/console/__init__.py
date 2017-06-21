"""Console Plugin Init.
"""
from pytsite import lang as _lang
from ._command import Command
from . import _error as error, _option as option
from . import _help


# Public API
from ._api import register_command, get_command, run_command, usage, run, print_info, print_error, print_success, \
    print_warning


__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


_lang.register_package(__name__)
register_command(_help.Help())
