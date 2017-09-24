"""ODM errors.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class ModelAlreadyRegistered(Exception):
    pass


class ModelNotRegistered(Exception):
    pass


class ReferenceNotFound(Exception):
    pass


class EntityNotFound(Exception):
    def __init__(self, model: str, eid: str):
        self._model = model
        self._eid = eid

    @property
    def model(self) -> str:
        return self._model

    @property
    def eid(self) -> str:
        return self._eid

    def __str__(self):
        return "Entity '{}:{}' is not found in database".format(self._model, self._eid)


class EntityNotStored(Exception):
    pass


class FieldNotDefined(Exception):
    def __init__(self, model: str, field_name: str):
        super().__init__()

        self._model = model
        self._field_name = field_name

    def __str__(self) -> str:
        return "Field '{}' is not defined in model '{}'".format(self._field_name, self._model)


class EntityDeleted(Exception):
    pass


class EntityNotLocked(Exception):
    pass


class FieldEmpty(Exception):
    pass


class NoCachedData(Exception):
    pass
