"""ODM models.
"""
from typing import Any as _Any
from abc import ABC as _ABC, abstractmethod as _abstractmethod
from collections import OrderedDict as _OrderedDict
from datetime import datetime as _datetime
from pymongo import ASCENDING as I_ASC, DESCENDING as I_DESC, GEO2D as I_GEO2D, TEXT as I_TEXT
from bson.objectid import ObjectId as _ObjectId
from bson.dbref import DBRef as _DBRef
from pymongo.collection import Collection as _Collection
from pymongo.errors import OperationFailure as _OperationFailure
from pytsite import db as _db, events as _events, threading as _threading, lang as _lang
from . import _error, _field

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Model(_ABC):
    """ODM Model.
    """
    def __init__(self, model: str, obj_id=None):
        """Init.

        :type model: str
        :type obj_id: str | _ObjectId
        """
        if not hasattr(self, 'collection_name'):
            self._collection_name = None

        if self._collection_name is None:
            if model[-1:] in ('s', 'h'):
                self._collection_name = model + 'es'
            else:
                self._collection_name = model + 's'

        self._is_new = True
        self._is_deleted = False
        self._indexes = []
        self._has_text_index = False

        self._fields = _OrderedDict()
        """:type: dict[str, _field.Abstract]"""

        self._define_field(_field.ObjectId('_id'))
        self._define_field(_field.String('_model', default=model))
        self._define_field(_field.Ref('_parent', model=model))
        self._define_field(_field.RefsList('_children', model=model))
        self._define_field(_field.DateTime('_created'))
        self._define_field(_field.DateTime('_modified'))

        # setup() hook
        self._setup()

        # Automatically create indices on new collections
        if self._collection_name not in _db.get_collection_names():
            self._create_indexes()

        # Loading fields data from collection
        if obj_id:
            # Load data from from DB
            self._load_data(obj_id)

            # Of course, loaded entity cannot be 'new'
            self._is_new = False
        else:
            # Filling fields with initial values
            self.f_set('_created', _datetime.now())
            self.f_set('_modified', _datetime.now())

    def _load_data(self, obj_id):
        """Load data from database.

        :type obj_id: _ObjectId | str
        """
        if isinstance(obj_id, str):
            obj_id = _ObjectId(obj_id)

        data = self.collection.find_one({'_id': obj_id})

        # No data has been found
        if not data:
            raise _error.EntityNotFound("Entity '{}:{}' is not found in storage.".format(self.model, str(obj_id)))

        # Filling fields with retrieved data
        for field_name, value in data.items():
            if self.has_field(field_name):
                self.get_field(field_name).set_val(value, False)

    def _define_index(self, fields, unique=False):
        """Define an index.

        :param fields: list|tuple
        """
        if isinstance(fields, tuple):
            fields = [fields]

        for item in fields:
            if not isinstance(item, tuple):
                raise TypeError("'fields' argument must be a list of tuples.")
            if len(item) != 2:
                raise ValueError("Field definition tuple must have exactly 2 members.")

            field_name, index_type = item
            if not self.has_field(field_name.split('.')[0]):
                raise Exception("Entity {} doesn't have field {}.".format(self.model, field_name))
            if index_type not in [I_ASC, I_DESC, I_GEO2D, I_TEXT]:
                raise ValueError("Invalid index type.")

            opts = {
                'unique': unique
            }

            if index_type == I_TEXT:
                self._has_text_index = True
                opts['language_override'] = 'language_db'

            self._indexes.append((fields, opts))

    def _define_field(self, field_obj: _field.Abstract):
        """Define a field.
        """
        if self.has_field(field_obj.name):
            raise Exception("Field '{}' already defined in model '{}'.".format(field_obj.name, self.model))
        self._fields[field_obj.name] = field_obj

        return self

    def _remove_field(self, field_name: str):
        """Remove field definition.
        """
        if not self.has_field(field_name):
            raise Exception("Field '{}' is not defined in model '{}'.".format(field_name, self.model))
        del self._fields[field_name]

    def _create_indexes(self):
        """Create indices.
        """
        for index_data in self._indexes:
            self.collection.create_index(index_data[0], **index_data[1])

    @property
    def indexes(self) -> dict:
        """Get index information.
        """
        return self._indexes

    @property
    def has_text_index(self) -> bool:
        return self._has_text_index

    def reindex(self):
        """Rebuild indices.
        """
        try:
            # Drop existing indices
            indices = self.collection.index_information()
            for i_name, i_val in indices.items():
                if i_name != '_id_':
                    self.collection.drop_index(i_name)
        except _OperationFailure:  # Collection does not exist in database
            pass

        self._create_indexes()

    def reload(self):
        """Reload entity data from database.
        """
        if self.is_new:
            return

        self._load_data(self.id)

    @_abstractmethod
    def _setup(self):
        """setup() hook.
        """
        pass

    def _check_deletion(self):
        if self.is_deleted:
            raise _error.EntityDeleted('Entity has been deleted.')

    def has_field(self, field_name: str) -> bool:
        """Check if the entity has field.
        """
        self._check_deletion()

        return False if field_name not in self._fields else True

    def get_field(self, field_name) -> _field.Abstract:
        """Get field's object.
        """
        self._check_deletion()

        if not self.has_field(field_name):
            raise _error.FieldNotDefined("Field '{}' is not defined in model '{}'.".format(field_name, self.model))

        return self._fields[field_name]

    @property
    def collection(self) -> _Collection:
        """Get entity's collection.
        """
        self._check_deletion()

        return _db.get_collection(self._collection_name)

    @property
    def fields(self) -> _OrderedDict:
        """Get all field objects.
        """
        self._check_deletion()

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
        self._check_deletion()

        if not self.id:
            raise _error.EntityNotStored('Entity must be stored before you can get its ref.')

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
    def children(self):
        """Get children entities.

        :rtype: typing.Tuple[Model]
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

    @property
    def is_new(self) -> bool:
        """Is the entity new or already stored in a database?
        """
        with _threading.get_r_lock():
            self._check_deletion()
            return self._is_new

    @property
    def is_modified(self) -> bool:
        """Is the entity has been modified?
        """
        with _threading.get_r_lock():
            self._check_deletion()
            for field_name, field in self._fields.items():
                if field.is_modified:
                    return True
            return False

    @property
    def is_deleted(self) -> bool:
        """Is the entity has been deleted?
        """
        with _threading.get_r_lock():
            return self._is_deleted

    def f_set(self, field_name: str, value, update_state=True, **kwargs):
        """Set field's value.
        """
        with _threading.get_r_lock():
            self._check_deletion()
            value = self._on_f_set(field_name, value, **kwargs)
            self.get_field(field_name).set_val(value, update_state, **kwargs)

        return self

    def _on_f_set(self, field_name: str, value, **kwargs):
        """On set field's value hook.
        """
        return value

    def f_get(self, field_name: str, **kwargs):
        """Get field's value.
        """
        with _threading.get_r_lock():
            self._check_deletion()
            field_val = self.get_field(field_name).get_val(**kwargs)
            field_val = self._on_f_get(field_name, field_val, **kwargs)
            return field_val

    def _on_f_get(self, field_name: str, value, **kwargs):
        """On get field's value hook.
        """
        return value

    def f_add(self, field_name: str, value, update_state=True, **kwargs):
        """Add a value to the field.
        """
        with _threading.get_r_lock():
            self._check_deletion()
            value = self._on_f_add(field_name, value, **kwargs)
            self.get_field(field_name).add_val(value, update_state, **kwargs)
            return self

    def _on_f_add(self, field_name: str, value, **kwargs):
        """On field's add value hook.
        """
        return value

    def f_sub(self, field_name: str, value, update_state=True, **kwargs):
        """Subtract value from the field.
        """
        with _threading.get_r_lock():
            self._check_deletion()
            value = self._on_f_sub(field_name, value, **kwargs)
            self.get_field(field_name).sub_val(value, update_state, **kwargs)
            return self

    def _on_f_sub(self, field_name: str, value, **kwargs) -> _Any:
        """On field's subtract value hook.
        """
        return value

    def f_inc(self, field_name: str, update_state=True, **kwargs):
        """Increment value of the field.
        """
        with _threading.get_r_lock():
            self._check_deletion()
            self._on_f_inc(field_name, **kwargs)
            self.get_field(field_name).inc_val(update_state, **kwargs)
            return self

    def _on_f_inc(self, field_name: str, **kwargs):
        """On field's increment value hook.
        """
        pass

    def f_dec(self, field_name: str, update_state=True, **kwargs):
        """Decrement value of the field
        """
        with _threading.get_r_lock():
            self._check_deletion()
            self._on_f_dec(field_name, **kwargs)
            self.get_field(field_name).dec_val(update_state, **kwargs)
            return self

    def _on_f_dec(self, field_name: str, **kwargs):
        """On field's decrement value hook.
        """
        pass

    def f_clr(self, field_name: str, update_state=True, **kwargs):
        """Creal field.
        """
        with _threading.get_r_lock():
            self._check_deletion()
            self._on_f_clr(field_name, **kwargs)
            self.get_field(field_name).clr_val(update_state, **kwargs)
            return self

    def _on_f_clr(self, field_name: str, **kwargs):
        """On field's clear value hook.
        """
        pass

    def f_is_empty(self, field_name: str) -> bool:
        """Checks if the field is empty.
        """
        with _threading.get_r_lock():
            self._check_deletion()
            return self.get_field(field_name).is_empty

    def append_child(self, child):
        """Append child to the entity

        :type child: Model
        """
        with _threading.get_r_lock():
            self._check_deletion()
            child.f_set('_parent', self)
            self.f_add('_children', child)

        return self

    def remove_child(self, child):
        """Remove child from the entity.

        :type child: Model
        """
        with _threading.get_r_lock():
            self._check_deletion()
            self.f_sub('_children', child)
            child.f_clr('_parent')

        return self

    def save(self, skip_hooks: bool=False, update_timestamp: bool=True):
        """Save the entity.
        """
        self._check_deletion()

        # Don't save entity if it wasn't changed
        if not self.is_modified:
            return self

        with _threading.get_r_lock():
            # Pre-save hook
            if not skip_hooks:
                self._pre_save()
                _events.fire('pytsite.odm.entity.pre_save', entity=self)
                _events.fire('pytsite.odm.entity.pre_save.' + self.model, entity=self)

            # Updating change timestamp
            if update_timestamp:
                self.f_set('_modified', _datetime.now())

            # Getting storable data from each field
            data = {}
            for f_name, field in self._fields.items():
                if isinstance(field, _field.Virtual):
                    continue
                if field.nonempty and field.is_empty:
                    raise _error.FieldEmpty("Value of the field '{}' cannot be empty.".format(f_name))
                data[f_name] = field.get_storable_val()

            # Let DB to calculate object's ID
            if self._is_new:
                del data['_id']

            # Saving data into collection
            if self._is_new:
                self.collection.insert_one(data)
            else:
                self.collection.replace_one({'_id': data['_id']}, data)

            if not skip_hooks:
                _events.fire('pytsite.odm.entity.save', entity=self)
                _events.fire('pytsite.odm.entity.save.' + self.model, entity=self)

            # Getting assigned ID from MongoDB
            if self._is_new:
                self.f_set('_id', data['_id'])

            # After save hook
            if not skip_hooks:
                self._after_save()

            # Notifying fields about entity saving
            for f_name, field in self._fields.items():
                field.reset_modified()

            # Entity is not new anymore
            if self._is_new:
                from ._api import cache_put
                self._is_new = False
                cache_put(self)

            # Save children with updated '_parent' field
            for child in self.children:
                if child.is_modified:
                    child.save(True, False)

        return self

    def _pre_save(self):
        """Pre save hook.
        """
        pass

    def _after_save(self):
        """After save hook.
        """
        pass

    def delete(self, **kwargs):
        """Delete the entity.
        """
        self._check_deletion()

        with _threading.get_r_lock():
            # Pre delete hook
            _events.fire('pytsite.odm.entity.pre_delete', entity=self)
            _events.fire('pytsite.odm.entity.{}.pre_delete'.format(self.model), entity=self)
            self._pre_delete(**kwargs)

            # Notify fields about entity deletion
            for f_name, field in self._fields.items():
                field.on_entity_delete()

            # Get children to notify them abou parent deletion
            children = self.children

            # Actual deletion from storage
            if not self._is_new:
                self.collection.delete_one({'_id': self.id})
                from ._api import cache_delete
                cache_delete(self)

            # Clearing parent reference from orphaned children
            for child in children:
                child.f_clr('_parent').save()

            # After delete hook
            self._after_delete()
            _events.fire('pytsite.odm.entity.delete', entity=self)
            _events.fire('pytsite.odm.entity.{}.delete'.format(self.model), entity=self)

            self._is_deleted = True

        return self

    def _pre_delete(self, **kwargs):
        """Pre delete hook.
        """
        pass

    def _after_delete(self):
        """After delete hook.
        """
        pass

    @classmethod
    def package_name(cls) -> str:
        """Get instance's package name.
        """
        return '.'.join(cls.__module__.split('.')[:-1])

    @classmethod
    def t(cls, partly_msg_id: str, args: dict=None) -> str:
        """Translate a string in model context.
        """
        return _lang.t(cls.resolve_partly_msg_id(partly_msg_id), args)

    @classmethod
    def t_plural(cls, partly_msg_id: str, num: int=2) -> str:
        """Translate a string into plural form.
        """
        return _lang.t_plural(cls.resolve_partly_msg_id(partly_msg_id), num)

    @classmethod
    def resolve_partly_msg_id(cls, partly_msg_id: str) -> str:
        # Searching for translation up in hierarchy
        for super_cls in cls.__mro__:
            if issubclass(super_cls, Model):
                full_msg_id = super_cls.package_name() + '@' + partly_msg_id
                if _lang.is_translation_defined(full_msg_id):
                    return full_msg_id

        return cls.package_name() + '@' + partly_msg_id
