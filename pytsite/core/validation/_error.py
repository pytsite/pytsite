"""Validation Exceptions
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class ValidationError(ValueError):
    def __init__(self, msg_args: dict=None):
        self._msg_args = msg_args if msg_args else {}

    @property
    def msg_args(self) -> dict:
        return self._msg_args
