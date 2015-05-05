from inspect import isclass
from datetime import datetime
from pytsite.core import db
from bson.objectid import ObjectId
from bson.dbref import DBRef
from pymongo.collection import Collection
from pymongo.cursor import Cursor, CursorType
from abc import ABC
from .helpers import dd


class EntityNotFoundException(Exception):
    pass


class Field(ABC):
    """Base field.
    """
    def __init__(self, name: str, **kwargs):
        """Init.
        """
        self._name = name
        self._modified = False
        self._value = None
        self._options = kwargs

    def get_name(self):
        """Get name of the field.
        """
        return self._name

    def is_modified(self)->bool:
        """Is the field has been modified?
        """
        return self._modified

    def reset_modified(self):
        """Reset the 'modified' status of the field.
        """
        self._modified = False
        return self

    def get_options(self)->dict:
        """Get field's options.
        """
        return self._options

    def get_option(self, opt_name: str, default=None):
        """Get field's option.
        """
        if opt_name in self._options:
            return self._options[opt_name]
        return default

    def set_val(self, value, change_modified: bool=True):
        """Set value of the field.
        """
        self._value = value
        if change_modified and not self._modified:
            self._modified = True
        return self

    def get_val(self, **kwargs):
        """Get value of the field
        """
        return self._value

    def get_storable_val(self):
        """Get value suitable to store in a database.
        """
        if self.get_option('not_empty') and not self._value:
            raise Exception("Value of the field '{0}' cannot be empty.".format(self.get_name()))
        return self._value

    def clear_val(self, reset_modified: bool=True):
        """Clears a value of the field.
        """
        raise Exception("Not implemented yet.")

    def add_val(self, value, change_modified: bool=True):
        """Add a value to the field.
        """
        raise Exception("Not implemented yet.")

    def subtract_val(self, value, change_modified: bool=True):
        """Remove a value from the field.
        """
        raise Exception("Not implemented yet.")

    def increment_val(self, change_modified: bool=True):
        """Increment a value of the field.
        """
        raise Exception("Not implemented yet.")

    def decrement_val(self, change_modified: bool=True):
        """Increment a value of the field.
        """
        raise Exception("Not implemented yet.")

    def delete(self):
        """Entity will be deleted from storage.
        """
        pass


class ObjectIdField(Field):
    """ObjectId field.
    """
    def set_val(self, value, change_modified: bool=True):
        """Set value of the field.
        """
        if not isinstance(value, ObjectId):
            raise TypeError("ObjectId expected")

        return super().set_val(value, change_modified)


class List(Field):
    """List field.
    """
    def __init__(self, name: str, **kwargs):
        super().__init__(name, **kwargs)
        self._value = []

    def set_val(self, value: list, change_modified: bool=True):
        """Set value of the field.
        """
        if not isinstance(value, list):
            raise TypeError("List expected")

        return super().set_val(value, change_modified)


class RefField(Field):
    """DBRef field.
    """
    def set_val(self, value, change_modified: bool=True):
        """Set value of the field.
        """
        if value and not isinstance(value, DBRef) and not isinstance(value, Model):
            raise TypeError("Entity or DBRef expected, while {0} given.".format(type(value)))

        if isinstance(value, Model):
            value = value.ref()

        return super().set_val(value, change_modified)

    def get_val(self, **kwargs):
        """Get value of the field.
        """
        if isinstance(self._value, DBRef):
            referenced_entity = dispense_by_ref(self._value)
            if not referenced_entity:
                self.set_val(None)  # Updating field's value about missing entity
            return referenced_entity


class RefsListField(Field):
    """List of DBRefs field.
    """
    def __init__(self, name: str, **kwargs):
        super().__init__(name, **kwargs)
        self._value = []

    def set_val(self, value: list, change_modified: bool=True):
        """Set value of the field.
        """
        if not isinstance(value, list):
            raise TypeError("List of DBRefs or entities expected.")

        clean_value = []
        for item in value:
            if not isinstance(item, DBRef) and not isinstance(item, Model):
                raise TypeError("List of DBRefs or entities expected.")

            if isinstance(item, Model):
                clean_value.append(item.ref())
            elif isinstance(item, DBRef):
                clean_value.append(item)

        return super().set_val(clean_value, change_modified)

    def get_val(self, **kwargs):
        """Get value of the field.
        """
        r = []
        for ref in self._value:
            entity = dispense_by_ref(ref)
            if entity:
                r.append(entity)

        return r

    def add_val(self, value, change_modified: bool=True):
        """Add a value to the field.
        """
        if not isinstance(value, DBRef) and not isinstance(value, Model):
            raise TypeError("DBRef of entity expected.")

        if isinstance(value, DBRef):
            self._value.append(value)
        elif isinstance(value, Model):
            self._value.append(value.ref())

        if change_modified:
            self._modified = True

        return self


class DateTimeField(Field):
    """Datetime field.
    """
    def __init__(self, name: str, **kwargs):
        super().__init__(name, **kwargs)
        self._value = datetime(1970, 1, 1)

    def set_val(self, value: list, change_modified: bool=True):
        """Set value of the field.
        """
        if value and not isinstance(value, datetime):
            raise TypeError("DateTime or None expected")

        return super().set_val(value, change_modified)


class StringField(Field):
    """String field.
    """
    def __init__(self, name: str, **kwargs):
        super().__init__(name, **kwargs)
        self._value = ''

    def set_val(self, value: str, change_modified: bool=True):
        """Set value of the field.
        """
        if not isinstance(value, str):
            raise TypeError("Str expected.")

        return super().set_val(value, change_modified)


class Model:
    def __init__(self, model_name: str, obj_id=None):
        """Init.
        """
        if not hasattr(self, 'collection_name'):
            self._collection_name = None

        if self._collection_name is None:
            self._collection_name = model_name + 's'

        self._collection = db.get_collection(self._collection_name)
        self._is_new = True
        self._is_deleted = False
        self._fields = dict()

        self.define_field(ObjectIdField('_id'))
        self.define_field(StringField('_model'))
        self.define_field(RefField('_parent'))
        self.define_field(RefsListField('_children'))
        self.define_field(DateTimeField('_created'))
        self.define_field(DateTimeField('_modified'))

        # setup() hook
        self._setup()

        # Loading fields data from collection
        if obj_id:
            if isinstance(obj_id, str):
                obj_id = ObjectId(obj_id)
            data = self._collection.find_one({'_id': obj_id})
            if not data:
                raise EntityNotFoundException("Entity '{0}' is not found in storage.".format(model_name + ':' + obj_id))
            for field_name, value in data.items():
                if self.has_field(field_name):
                    self.get_field(field_name).set_val(value, False)
            self._is_new = False
        else:
            # Filling some fields with initial values
            self.get_field('_model').set_val(model_name)
            self.get_field('_created').set_val(datetime.now())
            self.get_field('_modified').set_val(datetime.now())

    def define_field(self, field_obj: Field):
        """Define a field.
        """
        if self.has_field(field_obj.get_name()):
            raise Exception("Field '{0}' already defined in model '{1}'.".format(field_obj.get_name(), self.model()))
        self._fields[field_obj.get_name()] = field_obj

        return self

    def _setup(self):
        """setup() hook.
        """
        pass

    def collection(self)->Collection:
        """Get MongoDB's collection.
        """
        return self._collection

    def has_field(self, name)->bool:
        """Check if the entity has field.
        """
        if name not in self._fields:
            return False
        return True

    def get_field(self, field_name)->Field:
        """Get field's object.
        """
        if not self.has_field(field_name):
            raise Exception("Unknown field '{0}' in model '{1}'".format(field_name, self.model()))
        return self._fields[field_name]

    def get_fields(self)->dict:
        """Get all field objects.
        """
        return self._fields

    def id(self)->ObjectId:
        """Get entity ID.
        """
        return self.f_get('_id')

    def ref(self):
        """Get entity's DBRef.
        """
        if self.is_new():
            raise Exception("Entity must be stored before it can has reference.")
        return DBRef(self.collection().name, self.id())

    def model(self)->str:
        """Get model name.
        """
        return self.f_get('_model')

    def parent(self):
        """Get parent entity.
        """
        return self.f_get('_parent')

    def children(self)->list:
        """Get children entities.
        """
        return self.f_get('_children')

    def created(self)->datetime:
        """Get created date/time.
        """
        return self.f_get('_created')

    def modified(self)->datetime:
        """Get modified date/time.
        """
        return self.f_get('_modified')

    def f_set(self, field_name: str, value):
        """Set field's value.
        """
        value = self._on_f_set(field_name, value)
        self.get_field(field_name).set_val(value)
        return self

    def _on_f_set(self, field_name: str, field_value):
        """On set field's value hook.
        """
        return field_value

    def f_get(self, field_name: str):
        """Get field's value.
        """
        return self._on_f_get(field_name, self.get_field(field_name).get_val())

    def _on_f_get(self, field_name: str, field_value):
        """On get field's value hook.
        """
        return field_value

    def f_add(self, field_name: str, value):
        """Add a value to the field.
        """
        self.get_field(field_name).add_val(self._on_f_add(field_name, value))
        return self

    def _on_f_add(self, field_name: str, value):
        """On field's add value hook.
        """
        return value

    def is_new(self)->bool:
        """Is the entity new or already stored in a database?
        """
        return self._is_new

    def is_modified(self)->bool:
        """Is the entity has been modified?
        """
        for field_name, field in self.get_fields().items():
            if field.is_modified():
                return True
        return False

    def is_deleted(self)->bool:
        """Is the entity has been deleted?
        """
        return self._is_deleted

    def save(self):
        """Save the entity.
        """
        if self.is_deleted():
            raise Exception("Entity has been deleted from the storage.")

        # Don't save entity if it wasn't changed
        if not self.is_modified():
            return self

        # Pre-save hook
        self._pre_save()

        # Updating change timestamp
        self.f_set('_modified', datetime.now())

        # Getting storable data from each field
        data = dict()
        for f_name, field in self._fields.items():
            data[f_name] = field.get_storable_val()

        # Let MongoDB to calculate object's ID
        if self.is_new():
            del data['_id']

        # Saving data into collection
        self._collection.save(data)

        # Getting assigned ID from MongoDB
        if self.is_new():
            self.f_set('_id', data['_id'])

        # After save hook
        self._after_save()

        for f_name, field in self._fields.items():
            field.reset_modified()

        # Entity is not new anymore
        if self.is_new():
            self._is_new = False

        return self

    def _pre_save(self):
        """Pre save hook.
        """
        pass

    def _after_save(self):
        """After save hook.
        """
        pass

    def delete(self):
        """Delete the entity.
        """

        # Pre delete hook
        self._pre_delete()

        # Notify fields about entity deletion
        for f_name, field in self._fields.items():
            field.delete()

        # Actual deletion from storage
        if not self.is_new():
            self.collection().delete_one({'_id': self.id()})
            _cache_delete(self)

        self._is_deleted = True

        # After delete hook
        self._after_delete()

        return self

    def _pre_delete(self):
        """Pre delete hook.
        """
        pass

    def _after_delete(self):
        """After delete hook.
        """
        pass


class Query:
    def __init__(self, model: Model):
        self._model = model
        self._criteria = dict()

    def _resolve_logical_op(self, op: str)->str:
        if op not in ('and', 'or', '$and', '$or'):
            raise TypeError("Invalid logical operator: '{0}'.".format(op))
        if not op.startswith('$'):
            op = '$' + op
        return op

    def _resolve_comparison_op(self, op: str)->str:
        if op in ('=', 'eq', '$eq'):
            return '$eq'
        elif op in ('>', 'gt', '$gt'):
            return '$gt'
        elif op in ('>=', 'gte', '$gte'):
            return '$gte'
        elif op in ('in', '$in'):
            return '$in'
        elif op in ('<', 'lt', '$lt'):
            return '$lt'
        elif op in ('<=', 'lte', '$lte'):
            return '$lte'
        elif op in ('!=', 'ne', '$ne'):
            return '$ne'
        elif op in ('nin', '$nin'):
            return '$nin'
        elif op in ('regex', '$regex'):
            return '$regex'
        else:
            raise TypeError("Invalid comparison operator: '{0}'.".format(op))

    def add_criteria(self, logical_op: str, field_name: str, comparison_op: str, arg):
        """Add find criteria"""
        field = self._model.get_field(field_name)
        logical_op = self._resolve_logical_op(logical_op)
        comparison_op = self._resolve_comparison_op(comparison_op)

        # Convert str to ObjectId if it's necessary
        if isinstance(field, ObjectIdField):
            if isinstance(arg, str):
                arg = ObjectId(arg)

        # Adding logical operator's dictionary to the criteria
        if logical_op not in self._criteria:
            self._criteria[logical_op] = []

        # Finally adding the criteria itself
        self._criteria[logical_op].append({field_name: {comparison_op: arg}})

    def get_criteria(self)->list:
        """Get criteria"""
        return self._criteria


class Result:
    def __init__(self, model_name: str, cursor: Cursor):
        self._model_name = model_name
        self._cursor = cursor

    def __iter__(self):
        return self

    def __next__(self):
        doc = next(self._cursor)
        return dispense(self._model_name, doc['_id'])


class Finder:
    def __init__(self, model_name: str):
        self._model_name = model_name
        self._model = dispense(model_name)
        self._query = Query(self._model)
        self._skip = 0
        self._limit = 0
        self._sort = None

    def where(self, field_name: str, comparison_op: str, arg):
        """Add '$and' criteria.
        """
        self._query.add_criteria('$and', field_name, comparison_op, arg)
        return self

    def or_where(self, field_name: str, comparison_op: str, arg):
        """Add '$or' criteria
        """
        self._query.add_criteria('$or', field_name, comparison_op, arg)
        return self

    def skip(self, num: int):
        """Set number of records to skip in result cursor.
        """
        self._skip = num
        return self

    def sort(self, fields: list=None):
        """Set sort criteria.
        """
        for f in fields:
            if not self._model.has_field(f[0]):
                raise Exception("Unknown field '{0}' in model '{1}'".format(f[0], self._model_name))
        self._sort = fields
        return self

    def get(self, limit: int=0)->list:
        """Execute the query and return a cursor.
        """
        self._limit = limit
        collection = self._model.collection()
        cursor = collection.find(
            self._query.get_criteria(),
            {'_id': True},
            self._skip,
            self._limit,
            False,
            CursorType.NON_TAILABLE,
            self._sort
        )

        return Result(self._model_name, cursor)


__registered_models = dict()
__dispensed_entities = dict()


def register_model(model_name: str, model_class: type):
    """Register new ODM model.
    """
    if model_name in __registered_models:
        raise Exception("Model '{0}' already registered.".format(model_name))

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


def _cache_delete(entity: Model):
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