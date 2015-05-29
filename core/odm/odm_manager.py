__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from inspect import isclass
from pytsite.core import db, events
from bson.dbref import DBRef
from bson.objectid import ObjectId
from .errors import EntityNotFoundException
from .models import ODMModel

__registered_models = {}
__dispensed_entities = {}


def register_model(model: str, cls: type, replace: bool=False):
    """Register new ODM model.
    """

    if not isclass(cls):
        raise Exception("Class expected.")

    if not issubclass(cls, ODMModel):
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


def _cache_put(entity: ODMModel) -> ODMModel:
    """Put entity to the cache.
    """

    if not entity.is_new():
        cache_key = entity.model + ':' + str(entity.id)
        __dispensed_entities[cache_key] = entity

    return entity


def cache_delete(entity: ODMModel):
    """Delete entity from the cache.
    """

    if not entity.is_new():
        cache_key = entity.model + ':' + str(entity.id)
        if cache_key in __dispensed_entities:
            del __dispensed_entities[cache_key]


def dispense(model: str, entity_id=None) -> ODMModel:
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
    except EntityNotFoundException:
        return None

    # Cache entity if it has ID
    return _cache_put(entity)


def get_by_ref(ref: DBRef):
    """Dispense entity by DBRef.
    """

    doc = db.get_database().dereference(resolve_ref(ref))
    return dispense(doc['_model'], doc['_id']) if doc else None


def resolve_ref(something) -> DBRef:
    """Resolve DB object ref.

    :type something: str | ODMModel | DBRef
    :rtype: DBRef
    """

    if isinstance(something, DBRef):
        return something

    if isinstance(something, ODMModel):
        return something.ref

    if isinstance(something, str):
        parts = something.split(':')
        if len(parts) != 2:
            raise Exception('Invalid string reference format: {}'.format(something))

        model, uid = parts
        if not is_model_registered(model):
            raise Exception("Model '{}' is not registered.".format(model))

        return DBRef(dispense(model).collection.name, ObjectId(uid))

    raise Exception('Cannot resolve reference.')


def find(model_name: str):
    """Get ODM finder.
    """

    from .finder import Finder
    return Finder(model_name)
