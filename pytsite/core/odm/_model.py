"""ODM models.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from abc import ABC as _ABC, abstractmethod as _abstractmethod
from collections import OrderedDict as _OrderedDict
from datetime import datetime as _datetime
from pymongo import ASCENDING as I_ASC, DESCENDING as I_DESC, GEO2D as I_GEO2D
from bson.objectid import ObjectId as _ObjectId
from bson.dbref import DBRef as _DBRef
from pymongo.collection import Collection as _Collection
from pymongo.errors import OperationFailure as _OperationFailure
from pytsite.core import db as _db, events, lang
from . import _error, _field


class Model(_ABC):
    """ODM Model.
    """
    def __init__(self, model: str, obj_id=None):
        """Init.
        """
        if not hasattr(self, 'collection_name'):
            self._collection_name = None

        if self._collection_name is None:
            if model[-1:] in ('s', 'h'):
                self._collection_name = model + 'es'
            else:
                self._collection_name = model + 's'

        self._collection = _db.get_collection(self._collection_name)
        self._is_new = True
        self._is_deleted = False
        self._defined_indices = []

        self._fields = _OrderedDict()
        """:type: dict[str, _field.Abstract]"""

        self._define_field(_field.ObjectId('_id'))
        self._define_field(_field.String('_model', default=model))
        self._define_field(_field.Ref('_parent', model=model))
        self._define_field(_field.RefsListField('_children', model=model))
        self._define_field(_field.DateTime('_created'))
        self._define_field(_field.DateTime('_modified'))

        # setup() hook
        self._setup()

        # Automatically create indices on new collections
        if self._collection_name not in _db.get_collection_names():
            self._create_indices()

        # Loading fields data from collection
        if obj_id:
            if isinstance(obj_id, str):
                obj_id = _ObjectId(obj_id)
            data = self._collection.find_one({'_id': obj_id})
            if not data:
                raise _error.EntityNotFound("Entity '{0}' is not found in storage.".format(model + ':' + obj_id))
            for field_name, value in data.items():
                if self.has_field(field_name):
                    self.get_field(field_name).set_val(value, False)
            self._is_new = False
        else:
            # Filling some fields with initial values
            self.get_field('_model').set_val(model)
            self.get_field('_created').set_val(_datetime.now())
            self.get_field('_modified').set_val(_datetime.now())

    def _define_index(self, fields: list, unique=False):
        """Define an index.
        """
        for item in fields:
            if not isinstance(item, tuple):
                raise TypeError("'fields' argument must be a list of tuples.")
            if len(item) != 2:
                raise ValueError("Field definition tuple must have exactly 2 members.")

            field_name, index_type = item
            if not self.has_field(field_name.split('.')[0]):
                raise Exception("Entity {} doesn't have field {}.".format(self.model, field_name))
            if index_type not in [I_ASC, I_DESC, I_GEO2D]:
                raise ValueError("Invalid index type.")

            self._defined_indices.append((fields, {'unique': unique}))

    def _define_field(self, field_obj: _field.Abstract):
        """Define a field.
        """
        if self.has_field(field_obj.get_name()):
            raise Exception("Field '{}' already defined in model '{}'.".format(field_obj.get_name(), self.model))
        self._fields[field_obj.get_name()] = field_obj

        return self

    def _remove_field(self, field_name: str):
        """Remove field definition.
        """
        if not self.has_field(field_name):
            raise Exception("Field '{}' is not defined in model '{}'.".format(field_name, self.model))
        del self._fields[field_name]
        return self

    def _create_indices(self):
        """Create indices.
        """
        for index_data in self._defined_indices:
            self._collection.create_index(index_data[0], **index_data[1])

    def reindex(self):
        """Rebuild indices.
        """
        try:
            # Drop existing indices
            indices = self._collection.index_information()
            for i_name, i_val in indices.items():
                if i_name != '_id_':
                    self._collection.drop_index(i_name)

            self._create_indices()
        except _OperationFailure:  # Collection does not exist
            self._create_indices()

    @_abstractmethod
    def _setup(self):
        """setup() hook.
        """
        pass

    def has_field(self, name: str) -> bool:
        """Check if the entity has field.
        """
        if name not in self._fields:
            return False

        return True

    def get_field(self, field_name) -> _field.Abstract:
        """Get field's object.
        """
        if not self.has_field(field_name):
            raise Exception("Field '{}' is not defined in model '{}'.".format(field_name, self.model))
        return self._fields[field_name]

    @property
    def collection(self) -> _Collection:
        """Get entity's collection.
        """
        return self._collection

    @property
    def fields(self):
        """Get all field objects.

        ":rtype: int
        """
        return self._fields

    @property
    def id(self) -> _ObjectId:
        """Get entity ID.
        """
        return self.f_get('_id')

    @property
    def ref(self) -> _DBRef:
        """Get entity's DBRef.
        """
        if self._is_new:
            raise Exception("Entity must be stored first.")

        return _DBRef(self.collection.name, self.id)

    @property
    def model(self) -> str:
        """Get model name.
        """
        return self.f_get('_model')

    @property
    def parent(self):
        """Get parent entity.
        """
        return self.f_get('_parent')

    @property
    def children(self) -> list:
        """Get children entities.
        """
        return self.f_get('_children')

    @property
    def created(self) -> _datetime:
        """Get created date/time.
        """
        return self.f_get('_created')

    @property
    def modified(self) -> _datetime:
        """Get modified date/time.
        """
        return self.f_get('_modified')

    def f_set(self, field_name: str, value, **kwargs):
        """Set field's value.
        """
        value = self._on_f_set(field_name, value, **kwargs)
        self.get_field(field_name).set_val(value)

        return self

    def _on_f_set(self, field_name: str, value, **kwargs):
        """On set field's value hook.
        """
        return value

    def f_get(self, field_name: str, **kwargs):
        """Get field's value.
        """
        field_val = self.get_field(field_name).get_val(**kwargs)
        return self._on_f_get(field_name, field_val, **kwargs)

    def _on_f_get(self, field_name: str, value, **kwargs):
        """On get field's value hook.
        """
        return value

    def f_add(self, field_name: str, value):
        """Add a value to the field.
        """
        self.get_field(field_name).add_val(self._on_f_add(field_name, value))
        return self

    def _on_f_add(self, field_name: str, value, **kwargs: dict):
        """On field's add value hook.
        """
        return value

    def f_inc(self, field_name: str):
        """Increment value of the field.
        """
        self.get_field(field_name).inc_val()
        return self

    def f_dec(self, field_name: str):
        """Decrement value of the field
        """
        self.get_field(field_name).dec_val()
        return self

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
        self.f_set('_modified', _datetime.now())

        # Getting storable data from each field
        data = {}
        for f_name, field in self._fields.items():
            if isinstance(field, _field.Virtual):
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
        events.fire('odm.pre_delete', entity=self)
        events.fire('odm.pre_delete.' + self.model, entity=self)
        self._pre_delete()

        # Notify fields about entity deletion
        for f_name, field in self._fields.items():
            field.delete()

        # Actual deletion from storage
        if not self._is_new:
            self.collection.delete_one({'_id': self.id})
            from ._manager import cache_delete
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

    def package(self) -> str:
        """Get instance's package name.
        """
        return '.'.join(self.__class__.__module__.split('.')[:-1])

    def t(self, msg_id: str, args: dict=None) -> str:
        """Translate a string in model context.
        """
        return lang.t(self.package() + '@' + msg_id, args)

    def t_plural(self, msg_id: str, num: int=2) -> str:
        """Translate a string into plural form.
        """
        return lang.t_plural(self.package() + '@' + msg_id, num)
