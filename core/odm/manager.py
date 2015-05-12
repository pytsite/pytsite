__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


from pytsite.core import db
from bson.dbref import DBRef
from .errors import EntityNotFoundException
from .models import Model
from .finder import Finder


__registered_models = dict()
__dispensed_entities = dict()


def register_model(model_name: str, model_class: type):
    """Register new ODM model.
    """
    if model_name in __registered_models:
        raise Exception("Model '{0}' already registered.".format(model_name))

    from inspect import isclass
    if not isclass(model_class):
        raise Exception("Class required as second argument.")

    if not issubclass(model_class, Model):
        raise Exception("Subclassing of Model is required.")

    __registered_models[model_name] = model_class


def _cache_get(model_name: str, entity_id):
    """Get entity from the cache.
    """
    cache_key = model_name + ':' + str(entity_id)
    if cache_key in __dispensed_entities:
        cache_key = model_name + ':' + str(entity_id)
        return __dispensed_entities[cache_key]


def _cache_put(entity: Model)->Model:
    """Put entity to the cache.
    """
    if not entity.is_new():
        cache_key = entity.model() + ':' + str(entity.id())
        __dispensed_entities[cache_key] = entity
    return entity


def cache_delete(entity: Model):
    """Delete entity from the cache.
    """
    if not entity.is_new():
        cache_key = entity.model() + ':' + str(entity.id())
        if cache_key in __dispensed_entities:
            del __dispensed_entities[cache_key]


def dispense(model_name: str, entity_id=None)->Model:
    """Dispense an entity.
    """
    if model_name not in __registered_models:
        raise Exception("Model '{0}' is not registered".format(model_name))

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