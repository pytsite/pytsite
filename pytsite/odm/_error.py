"""ODM errors.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class ModelAlreadyRegistered(Exception):
    pass


class ModelNotRegistered(Exception):
    pass


class EntityNotFound(Exception):
    pass


class ForbidEntityDelete(Exception):
    pass


class FieldNotDefined(Exception):
    pass
