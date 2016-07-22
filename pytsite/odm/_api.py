"""ODM API Functions.
"""
from typing import Union as _Union, Iterable as _Iterable
from bson.dbref import DBRef as _DBRef
from bson.objectid import ObjectId as _ObjectId
from pytsite import db as _db, util as _util, events as _events, reg as _reg, cache as _cache, logger as _logger
from . import _model, _error, _finder

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_registered_models = {}
_cache_driver = _reg.get('odm.cache.driver', 'redis')
_finder_cache = {}
_dispensed_entities = {}
_dbg = _reg.get('odm.debug.api')


def register_model(model: str, cls: _Union[str, type], replace: bool = False):
    """Register new ODM model.
    """
    if isinstance(cls, str):
        cls = _util.get_class(cls)

    if not issubclass(cls, _model.Entity):
        raise TypeError("Unable to register model '{}': subclass of pytsite.odm.model.Entity expected."
                        .format(model))

    if is_model_registered(model) and not replace:
        raise _error.ModelAlreadyRegistered("Model '{}' already is registered.".format(model))

    # Create finder cache pool for each newly registered model
    if not replace:
        _finder_cache[model] = _cache.create_pool('pytsite.odm.finder:' + model, _cache_driver)

    _registered_models[model] = cls

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


def resolve_ref(something: _Union[str, _model.Entity, _DBRef, None], implied_model: str = None) -> _Union[_DBRef, None]:
    """Resolve DB object reference.
    """
    if isinstance(something, _DBRef) or something is None:
        return something

    elif isinstance(something, _model.Entity):
        return something.ref

    elif isinstance(something, str):
        something = something.strip()

        if not something:
            raise ValueError('Entity reference string is empty.')

        parts = something.split(':')
        if len(parts) != 2:
            raise ValueError('Invalid entity reference format string: {}.'.format(something))

        model, uid = parts
        if not is_model_registered(model):
            raise _error.ModelNotRegistered("Model '{}' is not registered.".format(model))

        return _DBRef(dispense(model).collection.name, _ObjectId(uid))

    elif isinstance(something, dict):
        if 'uid' not in something:
            raise ValueError('UID must be specified.')

        if not implied_model and 'model' not in something:
            raise ValueError('Model must be specified.')

        if 'model' not in something and implied_model == '*':
            raise ValueError('Model must be specified.')

        model = implied_model if implied_model else something['model']

        return resolve_ref('{}:{}'.format(model, something['uid']))

    raise ValueError('Cannot resolve reference.')


def resolve_refs(something: _Iterable, implied_model: str = None) -> list:
    r = []
    for v in something:
        r.append(resolve_ref(v, implied_model))

    return r


def get_by_ref(ref: _Union[str, _DBRef]) -> _Union[_model.Entity, None]:
    """Dispense entity by DBRef.
    """
    doc = _db.get_database().dereference(resolve_ref(ref))

    return dispense(doc['_model'], doc['_id']) if doc else None


def dispense(model: str, eid=None) -> _model.Entity:
    """Dispense an entity.
    """
    if not is_model_registered(model):
        raise _error.ModelNotRegistered("ODM model '{}' is not registered".format(model))

    model_class = get_model_class(model)

    if eid:
        c_key = '{}:{}'.format(model, eid)
        if c_key in _dispensed_entities:
            if _dbg:
                _logger.debug("Object of entity '{}' will be returned from the cache.".format(c_key))
            return _dispensed_entities[c_key]
        else:
            # Instantiate entity
            entity = model_class(model, eid)
            _dispensed_entities[c_key] = entity
            if _dbg:
                _logger.debug("Object of entity '{}' stored in the cache.".format(c_key))
                _logger.debug("Entity cache size: {}.".format(len(_dispensed_entities)))
    else:
        entity = model_class(model)
        if _dbg:
            _logger.debug("New entity of model '{}' dispensed.".format(model))

    return entity


def remove_from_cache(entity: _model.Entity):
    if entity.is_new:
        raise RuntimeError('You cannot remove non-stored entities.')

    c_key = '{}:{}'.format(entity.model, entity.id)
    if c_key in _dispensed_entities:
        del _dispensed_entities[c_key]

        if _dbg:
            _logger.debug("Object of the entity '{}' has been removed from the cache".format(entity.ref_str))
            _logger.debug("Entity cache size: {}.".format(len(_dispensed_entities)))


def find(model: str):
    """Get ODM finder.
    """
    return _finder.Finder(model, _cache.get_pool('pytsite.odm.finder:' + model))


def aggregate(model: str):
    from ._aggregation import Aggregator

    return Aggregator(model)


def get_finder_cache(model: str) -> _cache.driver.Abstract:
    return _cache.get_pool('pytsite.odm.finder:' + model)
