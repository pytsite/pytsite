"""ODM models.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from abc import ABC, abstractmethod
from pymongo import ASCENDING as I_ASC, DESCENDING as I_DESC
from pymongo.collection import Collection
from pymongo.errors import OperationFailure
from .. import db
from .errors import EntityNotFoundException
from .fields import *


class ODMModel(ABC):
    """ODM Model.
    """

    def __init__(self, model: str, obj_id=None):
        """Init.
        """
        if not hasattr(self, 'collection_name'):
            self._collection_name = None

        if self._collection_name is None:
            self._collection_name = model + 's'

        self._collection = db.get_collection(self._collection_name)
        self._is_new = True
        self._is_deleted = False
        self._indices = []
        self._fields = {}

        self._define_field(ObjectIdField('_id'))
        self._define_field(StringField('_model', default=model))
        self._define_field(RefField('_parent', model=model))
        self._define_field(RefsListField('_children', model=model))
        self._define_field(DateTimeField('_created'))
        self._define_field(DateTimeField('_modified'))

        # setup() hook
        self._setup()

        # Creating indices
        try:
            self._collection.index_information()
        except OperationFailure:
            for index_data in self._indices:
                self._collection.create_index(index_data[0], **index_data[1])

        # Loading fields data from collection
        if obj_id:
            if isinstance(obj_id, str):
                obj_id = ObjectId(obj_id)
            data = self._collection.find_one({'_id': obj_id})
            if not data:
                raise EntityNotFoundException("Entity '{0}' is not found in storage.".format(model + ':' + obj_id))
            for field_name, value in data.items():
                if self.has_field(field_name):
                    self.get_field(field_name).set_val(value, False)
            self._is_new = False
        else:
            # Filling some fields with initial values
            self.get_field('_model').set_val(model)
            self.get_field('_created').set_val(datetime.now())
            self.get_field('_modified').set_val(datetime.now())

    def _define_index(self, fields: list, unique=False):
        """Define an index.
        """
        for item in fields:
            if not isinstance(item, tuple):
                raise TypeError("'fields' argument must be list of tuples.")
            if len(item) != 2:
                raise ValueError("Field definition tuple must have exactly 2 members.")

            field_name, index_type = item
            if not self.has_field(field_name):
                raise Exception("Entity {0} doesn't have field {1}.".format(self.model, field_name))
            if index_type not in [I_ASC, I_DESC]:
                raise ValueError("Invalid index type.")

            self._indices.append((fields, {'unique': unique}))

    def _define_field(self, field_obj: AbstractField):
        """Define a field.
        """

        if self.has_field(field_obj.get_name()):
            raise Exception("Field '{0}' already defined in model '{1}'.".format(field_obj.get_name(), self.model))
        self._fields[field_obj.get_name()] = field_obj

        return self

    @abstractmethod
    def _setup(self):
        """setup() hook.
        """
        pass

    def has_field(self, name)->bool:
        """Check if the entity has field.
        """

        if name not in self._fields:
            return False

        return True

    def get_field(self, field_name) -> AbstractField:
        """Get field's object.
        """
        if not self.has_field(field_name):
            raise Exception("Unknown field '{0}' in model '{1}'".format(field_name, self.model))
        return self._fields[field_name]

    @property
    def collection(self) -> Collection:
        """Get entity's collection.
        """
        return self._collection

    @property
    def fields(self) -> dict:
        """Get all field objects.
        """
        return self._fields

    @property
    def id(self) -> ObjectId:
        """Get entity ID.
        """
        return self.f_get('_id')

    @property
    def ref(self) -> DBRef:
        """Get entity's DBRef.
        """

        if self._is_new:
            raise Exception("Entity must be stored before it can has reference.")

        return DBRef(self.collection.name, self.id)

    @property
    def model(self) -> str:
        """Get model name.
        """
        return self.f_get('_model')

    def parent(self):
        """Get parent entity.
        """
        return self.f_get('_parent')

    def children(self) -> list:
        """Get children entities.
        """
        return self.f_get('_children')

    def created(self, **kwargs) -> datetime:
        """Get created date/time.
        """
        return self.f_get('_created')

    def modified(self, **kwargs) -> datetime:
        """Get modified date/time.
        """
        return self.f_get('_modified')

    def f_set(self, field_name: str, value, **kwargs):
        """Set field's value.
        """
        value = self._on_f_set(field_name, value, **kwargs)
        self.get_field(field_name).set_val(value)

        return self

    def _on_f_set(self, field_name: str, orig_value, **kwargs):
        """On set field's value hook.
        """
        return orig_value

    def f_get(self, field_name: str, **kwargs):
        """Get field's value.
        """
        return self._on_f_get(field_name, self.get_field(field_name).get_val(**kwargs), **kwargs)

    def _on_f_get(self, field_name: str, orig_value, **kwargs):
        """On get field's value hook.
        """
        return orig_value

    def f_add(self, field_name: str, value):
        """Add a value to the field.
        """
        self.get_field(field_name).add_val(self._on_f_add(field_name, value))
        return self

    def _on_f_add(self, field_name: str, value, **kwargs: dict):
        """On field's add value hook.
        """
        return value

    @property
    def is_new(self) -> bool:
        """Is the entity new or already stored in a database?
        """
        return self._is_new

    @property
    def is_modified(self) -> bool:
        """Is the entity has been modified?
        """

        for field_name, field in self._fields.items():
            if field.is_modified():
                return True
        return False

    @property
    def is_deleted(self) -> bool:
        """Is the entity has been deleted?
        """
        return self._is_deleted

    def save(self):
        """Save the entity.
        """

        if self.is_deleted:
            raise Exception("Entity has been deleted from the storage.")

        # Don't save entity if it wasn't changed
        if not self.is_modified:
            return self

        # Pre-save hook
        self._pre_save()

        # Updating change timestamp
        self.f_set('_modified', datetime.now())

        # Getting storable data from each field
        data = dict()
        for f_name, field in self._fields.items():
            if isinstance(field, VirtualField):
                continue
            data[f_name] = field.get_storable_val()

        # Let MongoDB to calculate object's ID
        if self._is_new:
            del data['_id']

        # Saving data into collection
        if self._is_new:
            self._collection.insert_one(data)
        else:
            self._collection.replace_one({'_id': data['_id']}, data)

        # Getting assigned ID from MongoDB
        if self._is_new:
            self.f_set('_id', data['_id'])

        # After save hook
        self._after_save()

        # Notifying fields about entity saving
        for f_name, field in self._fields.items():
            field.reset_modified()

        # Entity is not new anymore
        if self._is_new:
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
        if not self._is_new:
            self.collection.delete_one({'_id': self.id})
            from .odm_manager import cache_delete
            cache_delete(self)

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
