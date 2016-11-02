"""PytSite GitHub Errors.
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class GeneralError(Exception):
    pass


class Unauthorized(GeneralError):
    pass


class Forbidden(GeneralError):
    pass


class NotFound(GeneralError):
    pass
