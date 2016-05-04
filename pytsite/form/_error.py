"""PytSite Form Errors.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class ValidationError(Exception):
    """Validation Error Exception.
    """
    def __init__(self, errors: dict):
        """Init.
        """
        self._errors = errors

    @property
    def errors(self) -> dict:
        return self._errors


class WidgetNotFound(Exception):
    pass
