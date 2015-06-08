"""ODM errors.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class EntityNotFound(Exception):
    pass


class ForbidEntityDelete(Exception):
    pass
