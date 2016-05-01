"""ODM API Functions.
"""
from typing import Union as _Union
from bson.dbref import DBRef as _DBRef
from bson.objectid import ObjectId as _ObjectId
from pytsite import db as _db, util as _util, events as _events
from . import _entity, _error, _finder

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_registered_models = {}


def register_model(model: str, cls: _Union[str, type], replace: bool = False):
    """Register new ODM model.
    """
    if isinstance(cls, str):
        cls = _util.get_class(cls)

    if not issubclass(cls, _entity.Entity):
        raise ValueError("Subclass of Model is expected.")

    if is_model_registered(model) and not replace:
        raise _error.ModelAlreadyRegistered("Model '{}' already is registered.".format(model))

    _registered_models[model] = cls

    if not replace:
        _finder.cache_create_pool(model)

    _events.fire('pytsite.odm.register_model', model=model, cls=cls, replace=replace)

    # Automatically create indices on new collections
    mock = dispense(model)
    if mock.collection.name not in _db.get_collection_names():
        mock.create_indexes()


def unregister_model(model: str):
    """Unregister model.
    """
    if not is_model_registered(model):
        raise _error.ModelNotRegistered("ODM model '{}' is not registered".format(model))

    del _registered_models[model]


def is_model_registered(model_name: str) -> bool:
    """Checks if the model already registered.
    """
    return model_name in _registered_models


def get_model_class(model: str) -> type:
    """Get registered class for model name.
    """
    if not is_model_registered(model):
        raise _error.ModelNotRegistered("ODM model '{}' is not registered".format(model))

    return _registered_models[model]


def get_registered_models() -> tuple:
    """Get registered models names.
    """
    return tuple(_registered_models.keys())


def resolve_ref(something: _Union[str, _entity.Entity, _DBRef, None]) -> _Union[_DBRef, None]:
    """Resolve DB object reference.
    """
    if isinstance(something, _DBRef) or something is None:
        return something

    if isinstance(something, _entity.Entity):
        return something.ref

    if isinstance(something, str):
        parts = something.split(':')
        if len(parts) != 2:
            raise ValueError('Invalid string reference format: {}'.format(something))

        model, uid = parts
        if not is_model_registered(model):
            raise _error.ModelNotRegistered("Model '{}' is not registered.".format(model))

        return _DBRef(dispense(model).collection.name, _ObjectId(uid))

    raise ValueError('Cannot resolve reference.')


def get_by_ref(ref: _Union[str, _DBRef]) -> _Union[_entity.Entity, None]:
    """Dispense entity by DBRef.
    """
    doc = _db.get_database().dereference(resolve_ref(ref))

    return dispense(doc['_model'], doc['_id']) if doc else None


def dispense(model: str, eid=None) -> _entity.Entity:
    """Dispense an entity.
    """
    if not is_model_registered(model):
        raise _error.ModelNotRegistered("ODM model '{}' is not registered".format(model))

    # Instantiate entity
    entity = get_model_class(model)(model, eid)

    return entity


def find(model: str):
    """Get ODM finder.
    """
    from ._finder import Finder

    return Finder(model)


def aggregate(model: str):
    from ._aggregation import Aggregator

    return Aggregator(model)
