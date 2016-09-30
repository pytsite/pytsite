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


class EntityNotStored(Exception):
    pass


class ForbidEntityOperation(Exception):
    pass


class FieldNotDefined(Exception):
    pass


class EntityDeleted(Exception):
    pass


class EntityNotLocked(Exception):
    pass


class FieldEmpty(Exception):
    pass


class NoCachedData(Exception):
    pass
