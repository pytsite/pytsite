"""PytSite Common Exceptions.
"""

__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Error(Exception):
    pass


class ForbidOperation(Error):
    pass


class ForbidCreation(ForbidOperation):
    pass


class ForbidModification(ForbidOperation):
    pass


class ForbidDeletion(ForbidOperation):
    pass


class NotFound(Error):
    pass
