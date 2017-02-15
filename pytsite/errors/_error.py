"""PytSite Common Exceptions.
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class ForbidOperation(RuntimeError):
    pass


class ForbidCreation(ForbidOperation):
    pass


class ForbidModification(ForbidOperation):
    pass


class ForbidDeletion(ForbidOperation):
    pass
