__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core import db, events, util
from bson.dbref import DBRef as _DBRef
from bson.objectid import ObjectId as _ObjectId
from . import _error, _model

__registered_models = {}
__dispensed_entities = {}


def register_model(model: str, cls, replace: bool=False):
    """Register new ODM model.

    :param cls: str|type
    """
    if isinstance(cls, str):
        cls = util.get_class(cls)

    if not issubclass(cls, _model.ODMModel):
        raise Exception("Subclass of Model is expected.")

    if is_model_registered(model) and not replace:
        raise Exception("Model '{}' already registered.".format(model))

    __registered_models[model] = cls

    events.fire('pytsite.core.odm@register_model', model=model, cls=cls)


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


def _cache_get(model_name: str, entity_id):
    """Get entity from the cache.
    """

    cache_key = model_name + ':' + str(entity_id)
    if cache_key in __dispensed_entities:
        cache_key = model_name + ':' + str(entity_id)
        return __dispensed_entities[cache_key]


def _cache_put(entity: _model.ODMModel) -> _model.ODMModel:
    """Put entity to the cache.
    """

    if not entity.is_new:
        cache_key = entity.model + ':' + str(entity.id)
        __dispensed_entities[cache_key] = entity

    return entity


def cache_delete(entity: _model.ODMModel):
    """Delete entity from the cache.
    """

    if not entity.is_new:
        cache_key = entity.model + ':' + str(entity.id)
        if cache_key in __dispensed_entities:
            del __dispensed_entities[cache_key]


def dispense(model: str, entity_id=None) -> _model.ODMModel:
    """Dispense an entity.
    """

    if not is_model_registered(model):
        raise Exception("ODM model '{}' is not registered".format(model))

    # Try to get entity from cache
    entity = _cache_get(model, entity_id)
    if entity:
        return entity

    # Dispense entity
    try:
        cls = get_model_class(model)
        entity = cls(model, entity_id)
    except _error.EntityNotFound:
        return None

    # Cache entity if it has ID
    return _cache_put(entity)


def get_by_ref(ref: _DBRef):
    """Dispense entity by DBRef.
    """
    doc = db.get_database().dereference(resolve_ref(ref))
    return dispense(doc['_model'], doc['_id']) if doc else None


def resolve_ref(something) -> _DBRef:
    """Resolve DB object ref.

    :type something: str | ODMModel | DBRef
    :rtype: DBRef
    """

    if isinstance(something, _DBRef):
        return something

    if isinstance(something, _model.ODMModel):
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
    from ._finder import ODMFinder
    return ODMFinder(model)


def distinct(self, model: str, field_name: str):
    """Get distinct values for field.
    """
    if not is_model_registered(model):
        raise Exception("ODM model '{}' is not registered".format(model))

    mock = dispense(model)
    if not mock.has_field(field_name.split('.')[0]):
        raise Exception("ODM model '{}' doesn't have field '{}'.".format(model, field_name))

    r = []
    for k, v in mock.collection.distinct(field_name):
        print(v)