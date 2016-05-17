"""ODM models.
"""
from typing import Any as _Any, Dict as _Dict, List as _List, Tuple as _Tuple, Union as _Union
from abc import ABC as _ABC, abstractmethod as _abstractmethod
from collections import OrderedDict as _OrderedDict
from datetime import datetime as _datetime
from pymongo import ASCENDING as I_ASC, DESCENDING as I_DESC, GEO2D as I_GEO2D, TEXT as I_TEXT, GEOSPHERE as I_GEOSPHERE
from bson.objectid import ObjectId as _ObjectId
from bson.dbref import DBRef as _DBRef
from bson import errors as _bson_errors
from frozendict import frozendict as _frozendict
from pymongo.collection import Collection as _Collection
from pymongo.errors import OperationFailure as _OperationFailure
from pytsite import db as _db, events as _events, mp as _mp, lang as _lang, logger as _logger, cache as _cache, \
    reg as _reg
from . import _error, _field

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_cache_driver = _reg.get('odm.cache.driver', 'redis')
_cache_pool = _cache.create_pool('pytsite.odm.entities', _cache_driver)
_dbg = _reg.get('odm.debug')


class Entity(_ABC):
    """ODM Model.
    """

    def __init__(self, model: str, obj_id=_Union[str, _ObjectId]):
        """Init.
        """
        if not hasattr(self, 'collection_name'):
            self._collection_name = None

        if self._collection_name is None:
            if model[-1:] in ('s', 'h'):
                self._collection_name = model + 'es'
            else:
                self._collection_name = model + 's'

        self._model = model
        self._id = None  # type: _ObjectId
        self._is_new = True
        self._is_modified = False
        self._is_deleted = False
        self._indexes = []
        self._has_text_index = False

        self._fields = _OrderedDict()  # type: _Dict[str, _field.Abstract]

        # Define 'system' fields
        self.define_field(_field.Ref('_parent', model=model))
        self.define_field(_field.RefsList('_children', model=model))
        self.define_field(_field.DateTime('_created'))
        self.define_field(_field.DateTime('_modified'))

        # Setup fields hook
        self._setup_fields()
        _events.fire('pytsite.odm.model.setup_fields', entity=self)
        _events.fire('pytsite.odm.model.{}.setup_fields'.format(model), entity=self)

        # Setup indexes hook
        self._setup_indexes()
        _events.fire('pytsite.odm.model.setup_indexes', entity=self)
        _events.fire('pytsite.odm.model.{}.setup_indexes'.format(model), entity=self)

        # Loading fields data from collection
        if obj_id:
            # Fill fields with data
            self._load_fields_data(obj_id)
        else:
            # Filling fields with initial values
            self.f_set('_created', _datetime.now())
            self.f_set('_modified', _datetime.now())

    def _get_lock(self):
        if self._is_new:
            raise RuntimeError('Non-saved entities cannot be locked.')

        return _mp.get_lock('pytsite.odm.{}.{}'.format(self.model, self.id), True)

    def lock(self, ttl: int = 10):
        """Lock the entity.
        """
        self._get_lock().lock(ttl)

    def unlock(self):
        """Unlock the entity.
        """
        self._get_lock().unlock()

    def _load_fields_data(self, eid: _Union[str, _ObjectId], skip_cache=False):
        """Load fields data from the cache or the database.
        """
        if isinstance(eid, str):
            eid = _ObjectId(eid)

        data_from_cache = False
        try:
            if not skip_cache:
                # Try to load data from cache:
                data = _cache_get(self._model, str(eid))
                data_from_cache = True
                if _dbg:
                    _logger.debug('Entity data LOADED from cache: {}:{}'.format(self._model, eid), __name__)
            else:
                raise _error.NoCachedData()

        except _error.NoCachedData:
            # Try to load fields data directly from DB
            data = self.collection.find_one({'_id': eid})
            if not data:
                raise _error.EntityNotFound("Entity '{}:{}' not found in the database.".format(self._model, str(eid)))

        # Filling fields with retrieved data
        self._fill_fields_data(data)

        # Of course, loaded entity cannot be 'new'
        self._is_new = False

        # Put fields data to cache
        if not data_from_cache:
            self._cache_push()
            if _dbg:
                _logger.debug('Entity data SAVED into cache: {}:{}'.format(self._model, eid), __name__)

    def _fill_fields_data(self, data: dict):
        """Fill fields with data.
        """
        for f_name, value in data.items():
            if f_name == '_id':
                self._id = value
            elif self.has_field(f_name):
                self.get_field(f_name).set_val(value)

    def define_index(self, definition: _List[_Tuple], unique=False):
        """Define an index.
        """
        opts = {
            'unique': unique
        }

        for item in definition:
            if not isinstance(item, tuple):
                raise TypeError("Model '{}'. List of tuples expected as index definition, got: '{}'".
                                format(self.model, definition))
            if len(item) != 2:
                raise ValueError("Index definition single item must have exactly 2 members.")

            field_name, index_type = item

            # Check for field existence
            if not self.has_field(field_name.split('.')[0]):
                raise Exception("Entity {} doesn't have field {}.".format(self.model, field_name))

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
            raise Exception("Field '{}' already defined in model '{}'.".format(field_obj.name, self.model))

        self._fields[field_obj.name] = field_obj

        return self

    def remove_field(self, field_name: str):
        """Remove field definition.
        """
        if not self.has_field(field_name):
            raise Exception("Field '{}' is not defined in model '{}'.".format(field_name, self.model))

        del self._fields[field_name]

    def create_indexes(self):
        """Create indices.
        """
        for index_data in self.indexes:
            self.collection.create_index(index_data[0], **index_data[1])

    @property
    def indexes(self) -> _frozendict:
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

    def reload(self):
        """Reload entity data from database.
        """
        if self._is_new:
            return

        self._load_fields_data(self.id, skip_cache=True)

    def _cache_push(self, check_empty_fields: bool = False):
        """Push fields data into cache.
        """
        if self._is_new:
            raise RuntimeError('Non-saved entities cannot be cached.')

        _cache_put(self._model, self._id, self.as_db_object(check_empty_fields))

    def _cache_pull(self):
        """Pull fields data from cache.
        """
        if self._is_new:
            raise RuntimeError('Non-saved entities cannot be cached.')

        try:
            self._fill_fields_data(_cache_get(self._model, self._id))

        except _error.NoCachedData:
            pass

    @_abstractmethod
    def _setup_fields(self):
        """Hook.
        """
        pass

    def _setup_indexes(self):
        """Hook.
        """
        pass

    def _check_deletion(self):
        """Raise an exception if the has 'deleted' state.
        """
        if self._is_deleted:
            raise _error.EntityDeleted('Entity has been deleted.')

    def has_field(self, field_name: str) -> bool:
        """Check if the entity has a field.
        """
        return False if field_name not in self._fields else True

    def get_field(self, field_name) -> _field.Abstract:
        """Get field's object.
        """
        if not self.has_field(field_name):
            raise _error.FieldNotDefined("Field '{}' is not defined in model '{}'.".format(field_name, self.model))

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
        self._check_deletion()

        if self._is_new:
            raise _error.EntityNotStored('Entity must be stored before you can get its ref.')

        return _DBRef(self.collection.name, self.id)

    @property
    def model(self) -> str:
        """Get model name.
        """
        return self._model

    @property
    def parent(self):
        """Get parent entity.
        """
        return self.f_get('_parent')

    @property
    def children(self):
        """Get children entities.

        :rtype: typing.Tuple[Entity]
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

    def f_set(self, field_name: str, value, update_state=True, **kwargs):
        """Set field's value.
        """
        if _dbg:
            _logger.debug("{}.f_set('{}'): {}".format(self.model, field_name, value), __name__)

        try:
            if not self._is_new:
                self.lock()

            hooked_val = self._on_f_set(field_name, value, **kwargs)
            if value is not None and hooked_val is None:
                raise RuntimeWarning("_on_f_set() for field '{}.{}' returned None.".format(self._model, field_name))

            self.get_field(field_name).set_val(hooked_val, **kwargs)

            if update_state:
                self._is_modified = True

            if not self._is_new and self._is_modified:
                self._cache_push()

        finally:
            if not self._is_new:
                self.unlock()

        return self

    def _on_f_set(self, field_name: str, value, **kwargs):
        """On set field's value hook.
        """
        return value

    def f_get(self, field_name: str, **kwargs):
        """Get field's value.
        """
        if _dbg:
            _logger.debug("{}.f_get('{}')".format(self.model, field_name), __name__)

        try:
            if not self._is_new:
                self.lock()
                self._cache_pull()

            # Get value
            orig_val = self.get_field(field_name).get_val(**kwargs)

            # Pass value through hook method
            hooked_val = self._on_f_get(field_name, orig_val, **kwargs)
            if orig_val is not None and hooked_val is None:
                raise RuntimeWarning("_on_f_get() for field '{}.{}' returned None.".format(self._model, field_name))

            return hooked_val

        finally:
            if not self._is_new:
                self.unlock()

    def _on_f_get(self, field_name: str, value, **kwargs):
        """On get field's value hook.
        """
        return value

    def f_add(self, field_name: str, value, update_state=True, **kwargs):
        """Add a value to the field.
        """
        if _dbg:
            _logger.debug("{}.f_add('{}'): {}".format(self.model, field_name, value), __name__)

        try:
            if not self._is_new:
                self.lock()
                self._cache_pull()

            value = self._on_f_add(field_name, value, **kwargs)
            self.get_field(field_name).add_val(value, **kwargs)

            if update_state:
                self._is_modified = True

            if not self._is_new and self._is_modified:
                self._cache_push()

        finally:
            if not self._is_new:
                self.unlock()

        return self

    def _on_f_add(self, field_name: str, value, **kwargs):
        """On field's add value hook.
        """
        return value

    def f_sub(self, field_name: str, value, update_state=True, **kwargs):
        """Subtract value from the field.
        """
        if _dbg:
            _logger.debug("{}.f_sub('{}'): {}".format(self.model, field_name, value), __name__)

        try:
            # Lock and load actual data from cache
            if not self._is_new:
                self.lock()
                self._cache_pull()

            # Call hook
            value = self._on_f_sub(field_name, value, **kwargs)

            # Subtract value from the field
            self.get_field(field_name).sub_val(value, **kwargs)

            if update_state:
                self._is_modified = True

            # Reflect changes to cache
            if not self._is_new and self._is_modified:
                self._cache_push()

        finally:
            if not self._is_new:
                self.unlock()

        return self

    def _on_f_sub(self, field_name: str, value, **kwargs) -> _Any:
        """On field's subtract value hook.
        """
        return value

    def f_inc(self, field_name: str, update_state=True, **kwargs):
        """Increment value of the field.
        """
        if _dbg:
            _logger.debug("{}.f_inc('{}')".format(self.model, field_name), __name__)

        try:
            if not self._is_new:
                self.lock()
                self._cache_pull()

            self._on_f_inc(field_name, **kwargs)
            self.get_field(field_name).inc_val(**kwargs)

            if update_state:
                self._is_modified = True

            if not self._is_new and self._is_modified:
                self._cache_push()

        finally:
            if not self._is_new:
                self.unlock()

        return self

    def _on_f_inc(self, field_name: str, **kwargs):
        """On field's increment value hook.
        """
        pass

    def f_dec(self, field_name: str, update_state=True, **kwargs):
        """Decrement value of the field
        """
        if _dbg:
            _logger.debug("{}.f_dec('{}')".format(self.model, field_name), __name__)

        try:
            if not self._is_new:
                self.lock()
                self._cache_pull()

            self._on_f_dec(field_name, **kwargs)
            self.get_field(field_name).dec_val(**kwargs)

            if update_state:
                self._is_modified = True

            if not self._is_new and self._is_modified:
                self._cache_push()

        finally:
            if not self._is_new:
                self.unlock()

        return self

    def _on_f_dec(self, field_name: str, **kwargs):
        """On field's decrement value hook.
        """
        pass

    def f_clr(self, field_name: str, update_state=True, **kwargs):
        """Clear field.
        """
        if _dbg:
            _logger.debug("{}.f_clr('{}')".format(self.model, field_name), __name__)

        try:
            if not self._is_new:
                self.lock()

            self._on_f_clr(field_name, **kwargs)
            self.get_field(field_name).clr_val(**kwargs)

            if update_state:
                self._is_modified = True

            if not self._is_new and self._is_modified:
                self._cache_push()

        finally:
            if not self._is_new:
                self.unlock()

        return self

    def _on_f_clr(self, field_name: str, **kwargs):
        """On field's clear value hook.
        """
        pass

    def f_is_empty(self, field_name: str) -> bool:
        """Checks if the field is empty.
        """
        if not self._is_new:
            self.lock()
            self._cache_pull()

        try:
            return self.get_field(field_name).is_empty
        finally:
            if not self._is_new:
                self.unlock()

    def append_child(self, child):
        """Append child to the entity

        :type child: Entity
        """
        if _dbg:
            _logger.debug('{}.append_child(): {}'.format(self.model, child), __name__)

        child.f_set('_parent', self)
        self.f_add('_children', child)

        return self

    def remove_child(self, child):
        """Remove child from the entity.

        :type child: Entity
        """
        if _dbg:
            _logger.debug('{}.remove_child(): {}'.format(self.model, child), __name__)

        self.f_sub('_children', child)
        child.f_clr('_parent')

        return self

    def save(self, skip_hooks: bool = False, update_timestamp: bool = True):
        """Save the entity.
        """
        # Don't save entity if it wasn't changed
        if not self._is_modified:
            return self

        if _dbg:
            _logger.debug('{}.save()'.format(self.model), __name__)

        if not self.is_new:
            self._check_deletion()
            self.lock()

        try:
            # Pre-save hook
            if not skip_hooks:
                self._pre_save()
                _events.fire('pytsite.odm.entity.pre_save', entity=self)
                _events.fire('pytsite.odm.entity.pre_save.' + self.model, entity=self)

            # Updating change timestamp
            if update_timestamp:
                self.f_set('_modified', _datetime.now())

            # Getting storable data from each field
            data = self.as_db_object()

            # Let DB to calculate object's ID
            if self._is_new:
                del data['_id']

            # Saving data into collection
            try:
                if self._is_new:
                    self.collection.insert_one(data)
                else:
                    self.collection.replace_one({'_id': data['_id']}, data)
            except _bson_errors.BSONError as e:
                _logger.error('BSON error: {}. Document dump: {}'.format(e, data), __name__)
                raise e

            if not skip_hooks:
                _events.fire('pytsite.odm.entity.save', entity=self)
                _events.fire('pytsite.odm.entity.save.' + self.model, entity=self)

            # Saved entity is not 'new'
            if self._is_new:
                self._id = data['_id']
                self._is_new = False

            # Saved entity is not 'modified'
            self._is_modified = False

            # After-save hook
            if not skip_hooks:
                self._cache_push(True)  # It is important to push cache before calling hook
                self._after_save()

            # Push cache
            self._cache_push(True)

            # Clear entire finder cache for this model
            from . import _finder
            _finder.cache_clear(self.model)

            # Save children with updated '_parent' field
            for child in self.children:
                if child.is_modified:
                    child.save(True, False)

        finally:
            if not self._is_new:
                self.unlock()

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
        if self._is_new:
            raise RuntimeError('New entities cannot be deleted.')

        if _dbg:
            _logger.debug('{}.delete()'.format(self.model), __name__)

        self._check_deletion()

        try:
            self.lock()

            # Pre delete hook
            _events.fire('pytsite.odm.entity.pre_delete', entity=self)
            _events.fire('pytsite.odm.entity.{}.pre_delete'.format(self.model), entity=self)
            self._pre_delete(**kwargs)

            # Notify fields about entity deletion
            for f_name, field in self._fields.items():
                field.on_entity_delete()

            # Get children to notify them about parent deletion
            children = self.children

            # Actual deletion from the database
            if not self._is_new:
                self.collection.delete_one({'_id': self.id})

            # Clearing parent reference from orphaned children
            for child in children:
                child.f_clr('_parent').save()

            # After delete hook
            self._after_delete()
            _events.fire('pytsite.odm.entity.delete', entity=self)
            _events.fire('pytsite.odm.entity.{}.delete'.format(self.model), entity=self)

            # Delete entity from cache
            _cache_rm(self._model, self.id)

            # Clear finder cache
            from . import _finder
            _finder.cache_clear(self.model)

            self._is_deleted = True

        finally:
            self.unlock()

        return self

    def _pre_delete(self, **kwargs):
        """Pre delete hook.
        """
        pass

    def _after_delete(self):
        """After delete hook.
        """
        pass

    def as_db_object(self, check_empty_fields: bool = True) -> dict:
        """Get storable representation of the entity.
        """
        r = {
            '_id': self._id,
            '_model': self._model,
        }

        for f_name, f in self.fields.items():
            if isinstance(f, _field.Virtual):
                continue

            # Required fields should be filled
            if check_empty_fields and f.nonempty and f.is_empty:
                raise _error.FieldEmpty("{}.{}: Value cannot be empty.".format(self.model, f_name))

            r[f_name] = f.get_storable_val()

        return r

    def as_dict(self, fields: tuple = (), **kwargs) -> _Dict:
        """Get dictionary representation of the entity.
        """
        r = {}
        for f_name in fields:
            if self.has_field(f_name):
                f = self.get_field(f_name)

                if isinstance(f, _field.Ref):
                    f_val = f.get_val()
                    if f_val:
                        sub_fields = tuple([sub_f_name.replace(f_name + '.', '')
                                            for sub_f_name in fields if sub_f_name.startswith(f_name + '.')])
                        r[f_name] = f_val.as_dict(sub_fields)
                elif isinstance(f, _field.Virtual):
                    r[f_name] = self.f_get(f_name)
                else:
                    r[f_name] = f.get_serializable_val()

        return r

    @classmethod
    def package_name(cls) -> str:
        """Get instance's package name.
        """
        return '.'.join(cls.__module__.split('.')[:-1])

    @classmethod
    def t(cls, partly_msg_id: str, args: dict = None) -> str:
        """Translate a string in model context.
        """
        return _lang.t(cls.resolve_partly_msg_id(partly_msg_id), args)

    @classmethod
    def t_plural(cls, partly_msg_id: str, num: int = 2) -> str:
        """Translate a string into plural form.
        """
        return _lang.t_plural(cls.resolve_partly_msg_id(partly_msg_id), num)

    @classmethod
    def resolve_partly_msg_id(cls, partly_msg_id: str) -> str:
        # Searching for translation up in hierarchy
        for super_cls in cls.__mro__:
            if issubclass(super_cls, Entity):
                full_msg_id = super_cls.package_name() + '@' + partly_msg_id
                if _lang.is_translation_defined(full_msg_id):
                    return full_msg_id

        return cls.package_name() + '@' + partly_msg_id

    def __eq__(self, other) -> bool:
        """__eq__ overloading.
        """
        if hasattr(other, 'ref') and self.ref == other.ref:
            return True

        return False


def _cache_has(model: str, eid: _Union[str, _ObjectId]) -> bool:
    if isinstance(eid, _ObjectId):
        eid = str(eid)

    return _cache_pool.has('{}:{}'.format(model, eid))


def _cache_get(model: str, eid: _Union[str, _ObjectId]) -> dict:
    """Build entity from cached data.
    """
    if isinstance(eid, _ObjectId):
        eid = str(eid)

    if not _cache_has(model, eid):
        raise _error.NoCachedData("No cached data for {}.{}".format(model, eid))

    return _cache_pool.get('{}:{}'.format(model, eid))


def _cache_put(model: str, eid: _Union[str, _ObjectId], data: dict):
    """Put entity data into the cache.
    """
    if isinstance(eid, _ObjectId):
        eid = str(eid)

    _cache_pool.put('{}:{}'.format(model, eid, data), data, 86400)


def _cache_rm(model: str, eid: _Union[str, _ObjectId]):
    """Remove item from the cache.
    """
    if isinstance(eid, _ObjectId):
        eid = str(eid)

    _cache_pool.rm('{}:{}'.format(model, eid))
