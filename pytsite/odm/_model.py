"""ODM Entity Model
"""
from typing import Any as _Any, Dict as _Dict, List as _List, Tuple as _Tuple, Union as _Union
from abc import ABC as _ABC, abstractmethod as _abstractmethod
from collections import OrderedDict as _OrderedDict
from datetime import datetime as _datetime
from pymongo import ASCENDING as I_ASC, DESCENDING as I_DESC, GEO2D as I_GEO2D, TEXT as I_TEXT, GEOSPHERE as I_GEOSPHERE
from pymongo import errors as _pymonog_errors
from bson.objectid import ObjectId as _ObjectId
from bson.dbref import DBRef as _DBRef
from bson import errors as _bson_errors
from pymongo.collection import Collection as _Collection
from pymongo.errors import OperationFailure as _OperationFailure
from pytsite import db as _db, events as _events, lang as _lang, logger as _logger, reg as _reg, errors as _errors, \
    util as _util, dlm as _dlm, cache as _cache
from . import _error, _field

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_DBG = _reg.get('odm.debug.entity')
_ENTITIES_CACHE = _cache.get_pool('pytsite.odm.entities')


class Entity(_ABC):
    """ODM Model.
    """

    def __init__(self, model: str, obj_id: _Union[str, _ObjectId, None] = None):
        """Init.
        """
        # Let developer to specify collection name manually
        if not hasattr(self, '_collection_name'):
            self._collection_name = None

        # Define collection name if it wasn't specified
        if self._collection_name is None:
            if model[-1:] in ('s', 'h'):
                self._collection_name = model + 'es'
            else:
                self._collection_name = model + 's'

        self._model = model
        self._id = None  # type: _ObjectId
        self._is_new = True
        self._is_modified = True
        self._is_being_deleted = False
        self._is_deleted = False
        self._indexes = []
        self._has_text_index = False
        self._lock_obj = _dlm.Lock(_util.random_str())

        self._fields = _OrderedDict()  # type: _Dict[str, _field.Abstract]

        # Define 'system' fields
        self.define_field(_field.Ref('_parent', model=model))
        self.define_field(_field.RefsList('_children', model=model))
        self.define_field(_field.Integer('_depth', required=True, default=0))
        self.define_field(_field.DateTime('_created', default=_datetime.now()))
        self.define_field(_field.DateTime('_modified', default=_datetime.now()))

        # Delegate fields setup process to the hook method
        self._setup_fields()
        _events.fire('pytsite.odm.model.setup_fields', entity=self)
        _events.fire('pytsite.odm.model.{}.setup_fields'.format(model), entity=self)

        # Delegate indexes setup process to the hook method
        self._setup_indexes()
        _events.fire('pytsite.odm.model.setup_indexes', entity=self)
        _events.fire('pytsite.odm.model.{}.setup_indexes'.format(model), entity=self)

        if obj_id:
            # Set entity's ID
            self._id = _ObjectId(obj_id) if isinstance(obj_id, str) else obj_id

            # Update lock object reference
            self._lock_obj = _dlm.Lock(self.ref_str)

            # Loading fields data from database or cache. Entity must be locked at this moment.
            with self:
                self._load_fields_data(obj_id)

    @classmethod
    def on_register(cls, model: str):
        pass

    def lock(self):
        """Lock the entity.
        """
        self._lock_obj.acquire()

        return self

    def unlock(self):
        """Unlock the entity.
        """
        if not self._lock_obj.locked:
            raise RuntimeError('Non-locked entity cannot be unlocked.')

        self._lock_obj.release()

        return self

    def _load_fields_data(self, eid: _Union[str, _ObjectId]):
        """Load fields data from the database
        """
        if isinstance(eid, str):
            eid = _ObjectId(eid)

        cache_key = '{}.{}'.format(self._model, eid)

        try:
            # Check if the entity fields data is in the cache
            _ENTITIES_CACHE.get_hash(cache_key)
        except _cache.error.KeyNotExist:
            # Get entity data from database and put in to the cache
            data = self.collection.find_one({'_id': eid})
            if not data:
                raise _error.EntityNotFound("Data for entity '{}:{}' is not found in database".format(self._model, eid))

            # Put fields data into cache
            _ENTITIES_CACHE.put_hash(cache_key, data)

        # Notify fields that they now can operate with data through cache
        for f_name in self.fields:
            field = self.get_field(f_name)
            field.uid = '{}.{}.{}'.format(self._model, eid, f_name)
            field.cache_key = cache_key

        # Of course, loaded entity cannot be 'new' and 'modified'
        self._is_new = False
        self._is_modified = False

        if _DBG:
            caller = _util.format_call_stack_str(' > ', 2)
            _logger.debug("[ENTITY DATA LOADED FROM DB] {}, called by {}".format(self.ref_str, caller))

    def define_index(self, definition: _List[_Tuple], unique=False):
        """Define an index.
        """
        opts = {
            'unique': unique
        }

        for item in definition:
            if not isinstance(item, tuple):
                raise TypeError("Model '{}'. List of tuples expected as index definition, got: '{}'".
                                format(self._model, definition))
            if len(item) != 2:
                raise ValueError("Index definition single item must have exactly 2 members.")

            field_name, index_type = item

            # Check for field existence
            if not self.has_field(field_name.split('.')[0]):
                raise RuntimeError("Entity {} doesn't have field {}.".format(self._model, field_name))

            # Check index type
            if index_type not in (I_ASC, I_DESC, I_GEO2D, I_TEXT, I_GEOSPHERE):
                raise ValueError("Invalid index type.")

            # Language field for text indexes
            if index_type == I_TEXT:
                self._has_text_index = True
                opts['language_override'] = 'language_db'

        self._indexes.append((definition, opts))

    def define_field(self, field_obj: _field.Abstract):
        """Define a field.
        """
        if self.has_field(field_obj.name):
            raise RuntimeError("Field '{}' already defined in model '{}'.".format(field_obj.name, self._model))

        self._fields[field_obj.name] = field_obj
        field_obj.entity = self

        return self

    def remove_field(self, field_name: str):
        """Remove field definition.
        """
        if not self.has_field(field_name):
            raise Exception("Field '{}' is not defined in model '{}'.".format(field_name, self._model))

        del self._fields[field_name]

    def create_indexes(self):
        """Create indices.
        """
        for index_data in self.indexes:
            self.collection.create_index(index_data[0], **index_data[1])

    @property
    def indexes(self) -> list:
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

        self.create_indexes()

    @_abstractmethod
    def _setup_fields(self):
        """Hook.
        """
        pass

    def _setup_indexes(self):
        """Hook.
        """
        pass

    def _check_is_not_deleted(self):
        """Raise an exception if the entity has 'deleted' state.
        """
        if self._is_deleted:
            raise _error.EntityDeleted("Entity '{}' has been deleted.".format(self.ref_str))

    def _check_is_locked(self):
        """Raise an exception if the entity is NOT locked.
        """
        if not self._is_new and not self._lock_obj.locked:
            raise _error.EntityNotLocked("Entity '{}' should be locked at this point.".format(self._model))

    def has_field(self, field_name: str) -> bool:
        """Check if the entity has a field.
        """
        return False if field_name not in self._fields else True

    def get_field(self, field_name: str) -> _field.Abstract:
        """Get field's object.
        """
        if not self.has_field(field_name):
            raise _error.FieldNotDefined("Field '{}' is not defined in model '{}'.".format(field_name, self._model))

        return self._fields[field_name]

    @property
    def collection(self) -> _Collection:
        """Get entity's collection.
        """
        return _db.get_collection(self._collection_name)

    @property
    def fields(self) -> _Dict[str, _field.Abstract]:
        """Get all field objects.
        """
        return self._fields

    @property
    def id(self) -> _Union[_ObjectId, None]:
        """Get entity ID.
        """
        return self._id

    @property
    def ref(self) -> _DBRef:
        """Get entity's DBRef.
        """
        self._check_is_not_deleted()

        if self._is_new:
            raise _error.EntityNotStored("Entity of model '{}' must be stored before you can get its ref."
                                         .format(self._model))

        return _DBRef(self.collection.name, self._id)

    @property
    def ref_str(self) -> str:
        if not self._id:
            raise _error.EntityNotStored("Entity of model '{}' must be stored before you can get its ref."
                                         .format(self._model))

        return '{}:{}'.format(self._model, self._id)

    @property
    def model(self) -> str:
        """Get model name.
        """
        return self._model

    @property
    def parent(self):
        """Get parent entity.
        :rtype: Entity
        """
        return self.f_get('_parent')

    @property
    def children(self):
        """Get children entities.

        :rtype: typing.Tuple[Entity]
        """
        return self.f_get('_children')

    @property
    def depth(self) -> int:
        """Get depth of the entity in children tree.
        """
        return self.f_get('_depth')

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
        """Is the entity stored in the database?
        """
        return self._is_new

    @property
    def is_modified(self) -> bool:
        """Is the entity has been modified?
        """
        return self._is_modified

    @property
    def is_deleted(self) -> bool:
        """Is the entity has been deleted?
        """
        return self._is_deleted

    @property
    def is_being_deleted(self) -> bool:
        """Is entity is being deleted?
        """
        return self._is_being_deleted

    def f_set(self, field_name: str, value, update_state: bool = True, **kwargs):
        """Set field's value.
        """
        self._check_is_locked()

        if _DBG:
            caller = _util.format_call_stack_str(' > ', 2)
            if self.is_new:
                _logger.debug("[NON-STORED ENTITY] {}.f_set('{}', {}), called by {}".
                              format(self._model, field_name, repr(value), caller))
            else:
                _logger.debug("[STORED ENTITY] {}.f_set('{}', {}), called by {}".
                              format(self.ref_str, field_name, repr(value), caller))

        hooked_val = self._on_f_set(field_name, value, **kwargs)
        if value is not None and hooked_val is None:
            raise RuntimeWarning("_on_f_set() for field '{}.{}' returned None".format(self._model, field_name))

        self.get_field(field_name).set_val(hooked_val, **kwargs)

        if update_state:
            self._is_modified = True

        return self

    def _on_f_set(self, field_name: str, value, **kwargs):
        """On set field's value hook.
        """
        return value

    def f_get(self, field_name: str, **kwargs):
        """Get field's value.
        """
        # Get value
        field = self.get_field(field_name)
        orig_val = field.get_val(**kwargs) if not isinstance(field, _field.Virtual) else None

        # Pass value through hook method
        hooked_val = self._on_f_get(field_name, orig_val, **kwargs)
        if orig_val is not None and hooked_val is None:
            raise RuntimeWarning("_on_f_get() for field '{}.{}' returned None".format(self._model, field_name))

        if _DBG:
            caller = _util.format_call_stack_str(' > ', 2)
            if self.is_new:
                _logger.debug("[ODM NON-STORED ENTITY] {}.f_get('{}') -> '{}', called by {}".
                              format(self._model, field_name, hooked_val, caller))
            else:
                _logger.debug("[ODM STORED ENTITY] {}.f_get('{}') -> '{}', called by {}".
                              format(self.ref_str, field_name, hooked_val, caller))

        return hooked_val

    def _on_f_get(self, field_name: str, value, **kwargs):
        """On get field's value hook.
        """
        return value

    def f_add(self, field_name: str, value, update_state=True, **kwargs):
        """Add a value to the field.
        """
        self._check_is_locked()

        if _DBG:
            caller = _util.format_call_stack_str(' > ', 2)
            if self.is_new:
                _logger.debug("[ODM NON-STORED ENTITY] {}.f_add('{}', {}), called by {}".
                              format(self._model, field_name, repr(value), caller))
            else:
                _logger.debug("[ODM STORED ENTITY] {}.f_add('{}', {}), called by {}".
                              format(self.ref_str, field_name, repr(value), caller))

        value = self._on_f_add(field_name, value, **kwargs)
        self.get_field(field_name).add_val(value, **kwargs)

        if update_state:
            self._is_modified = True

        return self

    def _on_f_add(self, field_name: str, value, **kwargs):
        """On field's add value hook.
        """
        return value

    def f_sub(self, field_name: str, value, update_state=True, **kwargs):
        """Subtract value from the field.
        """
        self._check_is_locked()

        if _DBG:
            caller = _util.format_call_stack_str(' > ', 2)
            if self.is_new:
                _logger.debug("[ODM NON-STORED ENTITY] {}.f_sub('{}', {}), called by {}".
                              format(self._model, field_name, repr(value), caller))
            else:
                _logger.debug("[ODM STORED ENTITY] {}.f_sub('{}', {}), called by {}".
                              format(self.ref_str, field_name, repr(value), caller))

        # Call hook
        value = self._on_f_sub(field_name, value, **kwargs)

        # Subtract value from the field
        self.get_field(field_name).sub_val(value, **kwargs)

        if update_state:
            self._is_modified = True

        return self

    def _on_f_sub(self, field_name: str, value, **kwargs) -> _Any:
        """On field's subtract value hook.
        """
        return value

    def f_inc(self, field_name: str, update_state=True, **kwargs):
        """Increment value of the field.
        """
        self._check_is_locked()

        if _DBG:
            caller = _util.format_call_stack_str(' > ', 2)
            if self.is_new:
                _logger.debug("[ODM NON-STORED ENTITY] {}.f_inc('{}'), called by {}".
                              format(self._model, field_name, caller))
            else:
                _logger.debug("[ODM STORED ENTITY] {}.f_inc('{}'), called by {}".
                              format(self.ref_str, field_name, caller))

        self._on_f_inc(field_name, **kwargs)
        self.get_field(field_name).inc_val(**kwargs)

        if update_state:
            self._is_modified = True

        return self

    def _on_f_inc(self, field_name: str, **kwargs):
        """On field's increment value hook.
        """
        pass

    def f_dec(self, field_name: str, update_state=True, **kwargs):
        """Decrement value of the field
        """
        self._check_is_locked()

        if _DBG:
            caller = _util.format_call_stack_str(' > ', 2)
            if self.is_new:
                _logger.debug("[ODM NON-STORED ENTITY] {}.f_dec('{}'), called by {}".
                              format(self._model, field_name, caller))
            else:
                _logger.debug("[ODM STORED ENTITY] {}.f_dec('{}'), called by {}".
                              format(self.ref_str, field_name, caller))

        self._on_f_dec(field_name, **kwargs)
        self.get_field(field_name).dec_val(**kwargs)

        if update_state:
            self._is_modified = True

        return self

    def _on_f_dec(self, field_name: str, **kwargs):
        """On field's decrement value hook.
        """
        pass

    def f_clr(self, field_name: str, update_state=True, **kwargs):
        """Clear field.
        """
        self._check_is_locked()

        if _DBG:
            caller = _util.format_call_stack_str(' > ', 2)
            if self.is_new:
                _logger.debug(
                    "[ODM NON-STORED ENTITY] {}.f_clr(), called by {}".format(self._model, field_name, caller))
            else:
                _logger.debug("[ODM STORED ENTITY] {}.f_clr(), called by {}".format(self.ref_str, field_name, caller))

        self._on_f_clr(field_name, **kwargs)
        self.get_field(field_name).clr_val()

        if update_state:
            self._is_modified = True

        return self

    def _on_f_clr(self, field_name: str, **kwargs):
        """On field's clear value hook.
        """
        pass

    def f_is_empty(self, field_name: str) -> bool:
        """Checks if the field is empty.
        """
        return self.get_field(field_name).is_empty

    def append_child(self, child):
        """Append child to the entity

        :type child: Entity
        """
        if child.is_new:
            raise RuntimeError('Entity should be saved before it can be as a child')

        self._check_is_locked()

        if _DBG:
            caller = _util.format_call_stack_str(' > ', 2)
            if self.is_new:
                _logger.debug('[ODM NON-STORED ENTITY] {}.append_child({}), called by {}'.
                              format(self._model, repr(child), caller))
            else:
                _logger.debug('[ODM STORED ENTITY] {}.append_child({}), called by {}'.
                              format(self.ref_str, repr(child), caller))

        with child:
            child.f_set('_parent', self)
            child.f_set('_depth', self.depth + 1)

        self.f_add('_children', child)

        return self

    def remove_child(self, child):
        """Remove child from the entity.

        :type child: Entity
        """
        self._check_is_locked()

        if _DBG:
            caller = _util.format_call_stack_str(' > ', 2)
            if self.is_new:
                _logger.debug('[ODM NON-STORED ENTITY] {}.remove_child({}), called by {}'.
                              format(self._model, repr(child), caller))
            else:
                _logger.debug('[ODM STORED ENTITY] {}.remove_child({}), called by {}'.
                              format(self.ref_str, repr(child), caller))

        self.f_sub('_children', child)
        child.f_clr('_parent')

        return self

    def save(self, **kwargs):
        """Save the entity.
        """
        self._check_is_locked()

        update_timestamp = kwargs.get('update_timestamp', True)

        # Don't save entity if it wasn't changed
        if not self._is_modified:
            return self

        if _DBG:
            caller = _util.format_call_stack_str(' > ', 2)
            if self.is_new:
                _logger.debug("[ODM NON-STORED ENTITY SAVE STARTED] {}, called by {}".format(self._model, caller))
            else:
                _logger.debug('[ODM STORED ENTITY SAVE STARTED] {}, called by {}'.format(self.ref_str, caller))

        # Pre-save hook
        self._pre_save()
        _events.fire('pytsite.odm.entity.pre_save', entity=self)
        _events.fire('pytsite.odm.entity.pre_save.' + self._model, entity=self)

        # Updating change timestamp
        if update_timestamp:
            self.f_set('_modified', _datetime.now())

        # Getting storable data of each field
        data = self.as_storable()

        # Let DB to calculate object's ID
        if self._is_new:
            del data['_id']

        # Save data into the database
        try:
            if self._is_new:
                self.collection.insert_one(data)
                if _DBG:
                    caller = _util.format_call_stack_str(' > ', 2)
                    _logger.debug('[ODM ENTITY DATA DB INSERT] {}: {}, called by {}'.
                                  format(self._model, data, caller))
            else:
                self.collection.replace_one({'_id': data['_id']}, data)
                if _DBG:
                    caller = _util.format_call_stack_str(' > ', 2)
                    _logger.debug('[ODM ENTITY DATA DB REPLACE] {}: {}, called by {}'.
                                  format(self.ref_str, data, caller))

        except (_bson_errors.BSONError, _pymonog_errors.PyMongoError) as e:
            _logger.error(e)
            _logger.error('Document dump: {}'.format(data))
            raise e

        # Update fields' UID so they can store values into shared cache
        if self._is_new:
            for f_name, f in self.fields.items():
                f.uid = '{}.{}.{}'.format(self._model, data['_id'], f_name)

        # Saved entity cannot be 'new'
        if self._is_new:
            first_save = True
            self._id = data['_id']
            self._is_new = False
        else:
            first_save = False

        # After-save hook
        self._after_save(first_save, **kwargs)
        _events.fire('pytsite.odm.entity.save', entity=self, first_save=first_save)
        _events.fire('pytsite.odm.entity.save.' + self._model, entity=self, first_save=first_save)

        # Saved entity is not 'modified'
        self._is_modified = False

        # Clear entire finder cache for the model
        from . import _api
        _api.get_finder_cache(self._model).clear()

        # Save children with updated '_parent' field
        if self.children:
            try:
                self.lock()
                for child in self.children:
                    with child:
                        child.save(update_timestamp=False)
            finally:
                self.unlock()

        if _DBG:
            caller = _util.format_call_stack_str(' > ', 2)
            _logger.debug('[ODM ENTITY SAVE FINISHED] {}.save() finished, called by {}'.format(self.ref_str, caller))

        return self

    def _pre_save(self, **kwargs):
        """Pre save hook.
        """
        pass

    def _after_save(self, first_save: bool = False, **kwargs):
        """After save hook.
        """
        pass

    def delete(self, **kwargs):
        """Delete the entity.
        """
        self._check_is_locked()

        if self._is_new:
            raise _errors.ForbidDeletion('Non stored entities cannot be deleted')

        if _DBG:
            caller = _util.format_call_stack_str(' > ', 2)
            _logger.debug('[ENTITY DELETE STARTED] {}, caller {}'.format(self.ref_str, caller))

        self._check_is_not_deleted()

        # Flag that deletion is in progress
        self._is_being_deleted = True

        # Pre delete events and hook
        _events.fire('pytsite.odm.entity.pre_delete', entity=self)
        _events.fire('pytsite.odm.entity.{}.pre_delete'.format(self._model), entity=self)
        self._pre_delete(**kwargs)

        # Notify each field about entity deletion
        for f_name, field in self._fields.items():
            field.on_entity_delete()

        # Get children to notify them about parent deletion
        children = self.children

        # Actual deletion from the database and cache
        self.collection.delete_one({'_id': self._id})

        # Clearing parent reference from orphaned children
        for child in children:
            with child:
                child.f_clr('_parent').save()

        # After delete events and hook. It is important to call them BEFORE entity entity data will be
        # completely removed from the cache
        self._after_delete(**kwargs)
        _events.fire('pytsite.odm.entity.delete', entity=self)
        _events.fire('pytsite.odm.entity.{}.delete'.format(self._model), entity=self)

        # Delete data from cache
        from . import _api
        _ENTITIES_CACHE.rm('{}.{}'.format(self._model, self._id))
        _api.get_finder_cache(self._model).clear()

        self._is_deleted = True
        self._is_being_deleted = False

        if _DBG:
            caller = _util.format_call_stack_str(' > ', 2)
            _logger.debug('[ENTITY DELETION FINISHED] {}, caller {}'.format(self.ref_str, caller))

        return self

    def _pre_delete(self, **kwargs):
        """Pre delete hook.
        """
        pass

    def _after_delete(self, **kwargs):
        """After delete hook.
        """
        pass

    def as_storable(self, check_required_fields: bool = True) -> dict:
        """Get storable representation of the entity
        """
        r = {
            '_id': self._id,
            '_model': self._model,
        }

        for f_name, f in self.fields.items():
            if isinstance(f, _field.Virtual):
                continue

            # Required fields should be filled
            if check_required_fields and f.required and f.is_empty:
                raise _error.FieldEmpty("Value of the field '{}.{}' cannot be empty".format(self._model, f_name))

            r[f_name] = f.internal_val

        return r

    def as_jsonable(self, **kwargs) -> _Dict:
        """Get JSONable dictionary representation of the entity.
        """
        return {
            'uid': str(self._id),
        }

    @classmethod
    def get_package_name(cls) -> str:
        """Get instance's package name.
        """
        return '.'.join(cls.__module__.split('.')[:-1])

    @classmethod
    def t(cls, partial_msg_id: str, args: dict = None) -> str:
        """Translate a string in model context.
        """
        return _lang.t(cls.resolve_msg_id(partial_msg_id), args)

    @classmethod
    def t_plural(cls, partial_msg_id: str, num: int = 2) -> str:
        """Translate a string into plural form.
        """
        return _lang.t_plural(cls.resolve_msg_id(partial_msg_id), num)

    @classmethod
    def resolve_msg_id(cls, partly_msg_id: str) -> str:
        # Searching for translation up in hierarchy
        for super_cls in cls.__mro__:
            if issubclass(super_cls, Entity):
                full_msg_id = super_cls.get_package_name() + '@' + partly_msg_id
                if _lang.is_translation_defined(full_msg_id):
                    return full_msg_id

        return cls.get_package_name() + '@' + partly_msg_id

    def __str__(self):
        """__str__ overloading.
        """
        return self.ref_str

    def __eq__(self, other) -> bool:
        """__eq__ overloading.
        """
        if isinstance(other, _DBRef):
            return self.ref == other
        elif hasattr(other, 'ref'):
            return self.ref == other.ref

        return False

    def __enter__(self):
        return self.lock()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.unlock()
