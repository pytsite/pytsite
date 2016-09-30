"""PytSite Common Exceptions.
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class ForbidCreation(RuntimeError):
    pass


class ForbidModification(RuntimeError):
    pass


class ForbidDeletion(RuntimeError):
    pass
