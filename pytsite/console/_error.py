"""Console Errors.
"""
from pytsite import lang as _lang

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Error(Exception):
    pass


class CommandNotFound(Error):
    pass


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


class InsufficientArguments(Error):
    def __str__(self):
        return _lang.t('pytsite.console@insufficient_arguments')


class TooManyArguments(Error):
    def __str__(self):
        return _lang.t('pytsite.console@too_many_arguments')


class MissingRequiredArgument(Error):
    def __init__(self, arg_name: str):
        self._arg_name = arg_name

    def __str__(self):
        return _lang.t('pytsite.console@required_argument_not_specified', {'arg_name': self._arg_name})
