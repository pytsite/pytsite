"""ODM API Functions
"""
from typing import Union as _Union, Iterable as _Iterable, Optional as _Optional
from bson.dbref import DBRef as _DBRef
from bson.objectid import ObjectId as _ObjectId
from pytsite import db as _db, util as _util, events as _events, reg as _reg, cache as _cache
from . import _model, _error, _finder

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_CACHE_DRIVER = _reg.get('odm.cache.driver', 'redis')
_ENTITIES_CACHE = _cache.get_pool('pytsite.odm.entities')
_MODELS = {}


def register_model(model: str, cls: _Union[str, type], replace: bool = False):
    """Register a new ODM model
    """
    if isinstance(cls, str):
        cls = _util.get_module_attr(cls)  # type: _model.Entity

    if not issubclass(cls, _model.Entity):
        raise TypeError("Unable to register model '{}': subclass of pytsite.odm.model.Entity expected."
                        .format(model))

    if is_model_registered(model) and not replace:
        raise _error.ModelAlreadyRegistered("Model '{}' is already registered.".format(model))

    # Create finder cache pool for each newly registered model
    if not replace:
        _cache.create_pool('pytsite.odm.finder.' + model, _CACHE_DRIVER)

    _MODELS[model] = cls

    cls.on_register(model)
    _events.fire('pytsite.odm.register', model=model, cls=cls, replace=replace)

    # Automatically create indices on new collections
    mock = dispense(model)
    if mock.collection.name not in _db.get_collection_names():
        mock.create_indexes()


def unregister_model(model: str):
    """Unregister model
    """
    if not is_model_registered(model):
        raise _error.ModelNotRegistered("ODM model '{}' is not registered".format(model))

    del _MODELS[model]


def is_model_registered(model_name: str) -> bool:
    """Checks if the model already registered
    """
    return model_name in _MODELS


def get_model_class(model: str) -> type:
    """Get registered class for model name
    """
    if not is_model_registered(model):
        raise _error.ModelNotRegistered("ODM model '{}' is not registered".format(model))

    return _MODELS[model]


def get_registered_models() -> tuple:
    """Get registered models names
    """
    return tuple(_MODELS.keys())


def resolve_ref(something: _Union[str, _model.Entity, _DBRef, None], implied_model: str = None) -> _Optional[_DBRef]:
    """Resolve DB object reference
    """
    if isinstance(something, _DBRef) or something is None:
        return something

    elif isinstance(something, _model.Entity):
        return something.ref

    elif isinstance(something, str):
        something = something.strip()

        if not something:
            raise ValueError('Entity reference string is empty')

        parts = something.split(':')
        if len(parts) != 2:
            raise ValueError('Invalid entity reference format string: {}.'.format(something))

        model, uid = parts
        if not is_model_registered(model):
            raise _error.ModelNotRegistered("Model '{}' is not registered.".format(model))

        return _DBRef(dispense(model).collection.name, _ObjectId(uid))

    elif isinstance(something, dict):
        if 'uid' not in something:
            raise ValueError('UID must be specified')

        if not implied_model and 'model' not in something:
            raise ValueError('Model must be specified')

        if 'model' not in something and implied_model == '*':
            raise ValueError('Model must be specified')

        model = implied_model if implied_model else something['model']

        return resolve_ref('{}:{}'.format(model, something['uid']))

    raise ValueError("Cannot resolve DB reference: '{}'".format(something))


def resolve_refs(something: _Iterable, implied_model: str = None) -> list:
    """Resolve multiple DB objects references
    """
    r = []
    for v in something:
        r.append(resolve_ref(v, implied_model))

    return r


def get_by_ref(ref: _Union[str, _DBRef]) -> _model.Entity:
    """Dispense entity by DBRef
    """
    doc = _db.get_database().dereference(resolve_ref(ref))

    if not doc:
        raise _error.ReferenceNotFound("Reference '{}' is not found in the database".format(ref))

    return dispense(doc['_model'], doc['_id'])


def dispense(model: str, uid: _Union[str, _ObjectId, None] = None) -> _model.Entity:
    """Dispense an entity
    """
    if not is_model_registered(model):
        raise _error.ModelNotRegistered("ODM model '{}' is not registered".format(model))

    model_class = get_model_class(model)

    # Get an existing entity
    if uid:
        return model_class(model, uid)

    # Create a new entity
    else:
        return model_class(model)


def find(model: str) -> _finder.Finder:
    """Get finder instance
    """
    return _finder.Finder(model, _cache.get_pool('pytsite.odm.finder.' + model))


def aggregate(model: str):
    """Get aggregator instance.
    """
    from ._aggregation import Aggregator

    return Aggregator(model)


def clear_finder_cache(model: str):
    """Get finder cache pool
    """
    _cache.get_pool('pytsite.odm.finder.' + model).clear()
    _events.fire('pytsite.odm.finder_cache.clear', model=model)
