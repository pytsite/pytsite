__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from inspect import isclass
from pytsite.core import db
from bson.dbref import DBRef
from .errors import EntityNotFoundException
from .model import ODMModel
from .finder import Finder

__registered_models = {}
__dispensed_entities = {}


def register_model(model_name: str, model_class: type):
    """Register new ODM model.
    """

    if is_model_registered(model_name):
        raise Exception("Model '{}' already registered.".format(model_name))

    if not isclass(model_class):
        raise Exception("Class expected.")

    if not issubclass(model_class, ODMModel):
        raise Exception("Subclass of Model is expected.")

    __registered_models[model_name] = model_class


def is_model_registered(model_name: str) -> bool:
    """Checks if the model already registered.
    """

    global __registered_models
    return model_name in __registered_models


def _cache_get(model_name: str, entity_id):
    """Get entity from the cache.
    """

    global __dispensed_entities
    cache_key = model_name + ':' + str(entity_id)
    if cache_key in __dispensed_entities:
        cache_key = model_name + ':' + str(entity_id)
        return __dispensed_entities[cache_key]


def _cache_put(entity: ODMModel)->ODMModel:
    """Put entity to the cache.
    """

    global __dispensed_entities
    if not entity.is_new():
        cache_key = entity.model() + ':' + str(entity.id())
        __dispensed_entities[cache_key] = entity
    return entity


def cache_delete(entity: ODMModel):
    """Delete entity from the cache.
    """

    global __dispensed_entities
    if not entity.is_new():
        cache_key = entity.model() + ':' + str(entity.id())
        if cache_key in __dispensed_entities:
            del __dispensed_entities[cache_key]


def dispense(model_name: str, entity_id=None)->ODMModel:
    """Dispense an entity.
    """
    if not is_model_registered(model_name):
        raise Exception("ODM model '{}' is not registered".format(model_name))

    # Try to get entity from cache
    entity = _cache_get(model_name, entity_id)
    if entity:
        return entity

    # Dispense entity
    try:
        entity = __registered_models[model_name](model_name, entity_id)
    except EntityNotFoundException:
        return None

    # Cache entity if it has ID
    return _cache_put(entity)


def dispense_by_ref(ref: DBRef):
    """Dispense entity by DBRef.
    """
    doc = db.get_database().dereference(ref)
    if not doc:
        return None
    return dispense(doc['_model'], doc['_id'])


def find(model_name: str)->Finder:
    """Get ODM finder.
    """
    return Finder(model_name)
