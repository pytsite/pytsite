"""Validation Exceptions.
"""
from pytsite import lang as _lang

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class RuleError(ValueError):
    def __init__(self, msg_id: str, msg_args: dict = None):
        self._msg_id = msg_id
        self._msg_args = msg_args

    @property
    def msg_id(self) -> str:
        return self._msg_id

    @property
    def msg_args(self) -> dict:
        return self._msg_args

    def __str__(self) -> str:
        return _lang.t(self._msg_id, self._msg_args)


class ValidatorError(ValueError):
    """Validation Error Exception.
    """

    def __init__(self, errors: dict):
        """Init.
        """
        self._errors = errors

    @property
    def errors(self) -> dict:
        return self._errors
