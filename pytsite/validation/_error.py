"""Validation Exceptions.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class ValidationError(ValueError):
    """Validation Error Exception.
    """
    def __init__(self, msg_args: dict=None):
        """Init.
        """
        self._msg_args = msg_args if msg_args else {}

    @property
    def msg_args(self) -> dict:
        """Get validation error message arguments.
        """
        return self._msg_args
