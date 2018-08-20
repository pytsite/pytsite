"""Console Errors
"""
from pytsite import lang as _lang

__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Error(Exception):
    pass


class CommandNotFound(Error):
    pass


class CommandExecutionError(Error):
    pass


class NoCommandRunning(Error):
    def __str__(self):
        return 'No console command currently running'


class MissingOption(Error):
    def __init__(self, opts_list: list):
        self._opts_list = opts_list

    def __str__(self):
        return _lang.t('pytsite.console@options_not_specified', {'opts_list': self._opts_list})


class MissingRequiredOption(Error):
    def __init__(self, opt_name: str):
        self._opt_name = opt_name

    def __str__(self):
        return _lang.t('pytsite.console@required_option_not_specified', {'opt_name': self._opt_name})


class InvalidOption(Error):
    def __init__(self, opt_name: str):
        self._opt_name = opt_name

    def __str__(self):
        return _lang.t('pytsite.console@invalid_option', {'opt_name': self._opt_name})


class InvalidArgument(Error):
    def __init__(self, arg_index: int, arg_value: str):
        self._arg_index = arg_index
        self._arg_value = arg_value

    def __str__(self):
        return _lang.t('pytsite.console@invalid_argument', {'arg_index': self._arg_index, 'arg_value': self._arg_value})


class MissingArgument(Error):
    def __init__(self, msg_id: str = None, arg_index: int = 0):
        self._msg_id = msg_id or 'pytsite.console@missing_argument'
        self._arg_index = arg_index

    def __str__(self):
        return _lang.t(self._msg_id, {'arg_index': self._arg_index})
