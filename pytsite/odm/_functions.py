from bson.dbref import DBRef as _DBRef
from bson.objectid import ObjectId as _ObjectId
from pytsite import db as _db, util as _util, threading as _threading, events as _events
from . import _model

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


__registered_models = {}
__dispensed_entities = {}


def register_model(model: str, cls, replace: bool=False):
    """Register new ODM model.

    :param cls: str|type
    """
    if isinstance(cls, str):
        cls = _util.get_class(cls)

    if not issubclass(cls, _model.Model):
        raise Exception("Subclass of Model is expected.")

    if is_model_registered(model) and not replace:
        raise Exception("Model '{}' already registered.".format(model))

    __registered_models[model] = cls

    _events.fire('pytsite.odm.register_model', model=model, cls=cls, replace=replace)


def get_model_class(model: str) -> type:
    """Get registered class for model name.
    """
    if not is_model_registered(model):
        raise Exception("ODM model '{}' is not registered".format(model))

    return __registered_models[model]


def is_model_registered(model_name: str) -> bool:
    """Checks if the model already registered.
    """
    return model_name in __registered_models


def get_registered_models() -> list:
    """Get registered models names.
    """
    return __registered_models.keys()


def _cache_get(model_name: str, entity_id):
    """Get entity from the cache.
    """
    if not entity_id:
        return

    cache_key = model_name + ':' + str(entity_id)
    if cache_key in __dispensed_entities:
        cache_key = model_name + ':' + str(entity_id)
        return __dispensed_entities[cache_key]


def cache_put(entity: _model.Model) -> _model.Model:
    """Put entity to the cache.
    """
    if not entity.is_new:
        cache_key = entity.model + ':' + str(entity.id)
        __dispensed_entities[cache_key] = entity

    return entity


def cache_delete(entity: _model.Model):
    """Delete entity from the cache.
    """
    if not entity.is_new:
        cache_key = entity.model + ':' + str(entity.id)
        if cache_key in __dispensed_entities:
            del __dispensed_entities[cache_key]


def dispense(model: str, entity_id=None) -> _model.Model:
    """Dispense an entity.
    """
    with _threading.get_r_lock():
        if not is_model_registered(model):
            raise Exception("ODM model '{}' is not registered".format(model))

        # Try to get entity from cache
        if entity_id:
            entity = _cache_get(model, entity_id)
            if entity:
                return entity

        # Instantiate Dispense entity
        entity = get_model_class(model)(model, entity_id)

        # Cache entity if it has ID
        return cache_put(entity)


def get_by_ref(ref: _DBRef):
    """Dispense entity by DBRef.
    """
    doc = _db.get_database().dereference(resolve_ref(ref))
    return dispense(doc['_model'], doc['_id']) if doc else None


def resolve_ref(something) -> _DBRef:
    """Resolve DB object ref.

    :type something: str | ODMModel | DBRef
    :rtype: DBRef
    """
    if isinstance(something, _DBRef):
        return something

    if isinstance(something, _model.Model):
        return something.ref

    if isinstance(something, str):
        parts = something.split(':')
        if len(parts) != 2:
            raise Exception('Invalid string reference format: {}'.format(something))

        model, uid = parts
        if not is_model_registered(model):
            raise Exception("Model '{}' is not registered.".format(model))

        return _DBRef(dispense(model).collection.name, _ObjectId(uid))

    raise Exception('Cannot resolve reference.')


def find(model: str):
    """Get ODM finder.
    """
    from ._finder import Finder
    return Finder(model)
