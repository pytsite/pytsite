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


class InvalidOption(Error):
    pass


class InsufficientArguments(Error):
    def __init__(self, *args, **kwargs):
        super().__init__(_lang.t('pytsite.console@insufficient_arguments'), *args, **kwargs)
