"""ODM Fields.
"""
from typing import Any as _Any, Iterable as _Iterable, Union as _Union
from abc import ABC as _ABC
from datetime import datetime as _datetime
from decimal import Decimal as _Decimal
from bson.dbref import DBRef as _bson_DBRef
from copy import deepcopy as _deepcopy
from frozendict import frozendict as _frozendict
from pytsite import lang as _lang, util as _util, cache as _cache, reg as _reg, logger as _logger

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_dbg = _reg.get('odm.debug.field')
_cache_pool = _cache.create_pool('pytsite.odm.fields')
_cache_storage_ttl = 600


class Abstract(_ABC):
    """Base field.
    """
    def __init__(self, name: str, **kwargs):
        """Init.

        :param default:
        :param nonempty: bool
        """
        self._name = name
        self._nonempty = kwargs.get('nonempty', False)
        self._default = _deepcopy(kwargs.get('default'))
        self._uid = None
        self._value = None

        # Set value to default
        self.clr_val()

    @property
    def nonempty(self) -> bool:
        return self._nonempty

    @nonempty.setter
    def nonempty(self, value: bool):
        self._nonempty = value

    @property
    def name(self) -> str:
        """Get name of the field.
        """
        return self._name

    @property
    def default(self) -> _Any:
        return self._default

    @default.setter
    def default(self, value):
        self._default = _deepcopy(value)

    @property
    def uid(self) -> str:
        return self._uid

    @uid.setter
    def uid(self, uid: str):
        prev_uid = self._uid
        self._uid = uid

        if _dbg:
            _logger.debug("Field's UID changed: {} -> {}".format(prev_uid, uid))

        # Update cached value after UID set/change
        _cache_pool.put(self._uid, self._value, _cache_storage_ttl)

    def _on_get(self, internal_value, **kwargs):
        """Hook. Transforms internal value to external one.
        """
        return internal_value

    def get_val(self, **kwargs) -> _Any:
        """Get value of the field.
        """
        # Get value from the cache if field has an UID
        if self._uid:
            try:
                self._value = _cache_pool.get(self._uid)
                if _dbg:
                    _logger.debug("[CACHED FIELD] {}.get_val() -> {}".format(self._uid, repr(self._value)))
            except _cache.error.KeyNotExist:
                # Update cached value if it expired or removed
                _cache_pool.put(self._uid, self._value)
        else:
            if _dbg:
                _logger.debug("[NON-CACHED FIELD] {}.get_val() -> {}".format(self.__class__, repr(self._value)))

        return self._on_get(self._value, **kwargs)

    def _on_get_storable(self, internal_value, **kwargs):
        """Hook.
        """
        return internal_value

    def as_storable(self, **kwargs):
        """Get value suitable to store in the database.
        """
        return self._on_get_storable(self._value, **kwargs)

    def _on_get_jsonable(self, internal_value, **kwargs):
        """Hook.
        """
        return internal_value

    def as_jsonable(self, **kwargs) -> _Union[int, str, float, bool, dict, tuple, list]:
        """Get JSONable representation of field's value.
        """
        return self._on_get_jsonable(self._value, **kwargs)

    def _on_set(self, value, **kwargs):
        """Hook. Transforms externally set value to internal value.
        """
        return value

    def set_val(self, value, **kwargs):
        """Set value of the field.
        """
        if value is None:
            value = _deepcopy(self._default)
        else:
            # Pass value through the hook
            value = self._on_set(value, **kwargs)

        # Always store internal value
        self._value = value

        # Store value to the cache if field has UID
        if self._uid:
            if _dbg:
                _logger.debug("[CACHED FIELD] {}.set_val({})".format(self._uid, repr(value)))
            _cache_pool.put(self._uid, self._value, _cache_storage_ttl)
        else:
            if _dbg:
                _logger.debug("[NON-CACHED FIELD] {}.{}.set_val({})".format(self.__class__, self.name, repr(value)))

        return self

    def clr_val(self, **kwargs):
        """Reset field's value to default.
        """
        return self.set_val(None, **kwargs)

    def _on_add(self, internal_value, value_to_add, **kwargs):
        """Hook.
        """
        return internal_value + value_to_add

    def add_val(self, value_to_add, **kwargs):
        """Add a value to the field.
        """
        return self.set_val(self._on_add(self._value, value_to_add, **kwargs), **kwargs)

    def _on_sub(self, internal_value, value_to_sub, **kwargs):
        """Hook.
        """
        return internal_value - value_to_sub

    def sub_val(self, value_to_sub, **kwargs):
        """Remove a value from the field.
        """
        return self.set_val(self._on_sub(self._value, value_to_sub, **kwargs), **kwargs)

    def _on_inc(self, **kwargs):
        """Hook.
        """
        raise ArithmeticError('Value of this field cannot be incremented.')

    def inc_val(self, **kwargs):
        """Increment a value of the field.
        """
        return self.set_val(self._value + self._on_inc(**kwargs), **kwargs)

    def _on_dec(self, **kwargs):
        """Hook.
        """
        raise ArithmeticError('Value of this field cannot be decremented.')

    def dec_val(self, **kwargs):
        """Increment a value of the field.
        """
        return self.set_val(self._value - self._on_dec(**kwargs), **kwargs)

    def on_entity_delete(self):
        """Hook method to provide for the entity notification mechanism about its deletion.
        """
        pass

    def __str__(self) -> str:
        """Stringify field's value.
        """
        return str(self.get_val())

    @property
    def is_empty(self) -> bool:
        return not bool(self.get_val())


class List(Abstract):
    """List field.
    """
    def __init__(self, name: str, **kwargs):
        """Init.
        """
        self._allowed_types = kwargs.get('allowed_types', (int, str, float, list, dict, tuple))
        self._min_len = kwargs.get('min_len')
        self._max_len = kwargs.get('max_len')
        self._unique = kwargs.get('unique', False)
        self._cleanup = kwargs.get('cleanup', True)

        kwargs['default'] = kwargs.get('default', [])

        super().__init__(name, **kwargs)

    def _on_get(self, internal_value, **kwargs) -> tuple:
        """Get value of the field.
        """
        return tuple(internal_value)

    def _on_set(self, value, **kwargs):
        """Set value of the field.

        :type value: list | tuple
        """
        if type(value) not in (list, tuple):
            raise TypeError("Field '{}': list or tuple expected, but {} given.".format(self._name, type(value)))

        # In internals value is always a list
        if isinstance(value, tuple):
            value = list(value)

        # Checking validness of types of the items
        if self._allowed_types:
            for v in value:
                if not isinstance(v, self._allowed_types):
                    raise TypeError("Value of the field '{}' cannot contain members of type {}, but only {}."
                                    .format(self.name, type(v), self._allowed_types))

        # Uniquize value
        if self._unique:
            clean_val = []
            for v in value:
                if v and v not in clean_val:
                    clean_val.append(v)
            value = clean_val

        # Checking lengths
        if self._min_len is not None and len(value) < self._min_len:
            raise ValueError("Value length cannot be less than {}.".format(self._min_len))
        if self._max_len is not None and len(value) > self._max_len:
            raise ValueError("Value length cannot be more than {}.".format(self._max_len))

        # Cleaning up empty string values
        if self._cleanup:
            value = _util.cleanup_list(value)

        return value

    def _on_add(self, internal_value, value_to_add, **kwargs):
        """Add a value to the field.
        """
        if not isinstance(value_to_add, self._allowed_types):
            raise TypeError("Value of the field '{}' cannot contain members of type {}, but only {}.".
                            format(self._name, type(value_to_add), self._allowed_types))

        # Checking length
        if self._max_len is not None and (len(internal_value) + 1) > self._max_len:
            raise ValueError("Value length cannot be more than {}.".format(self._max_len))

        r = internal_value

        # Checking for unique value
        if self._unique:
            if value_to_add not in r:
                r.append(value_to_add)
        else:
            if self._cleanup:
                # Cleaning up empty string values
                if isinstance(value_to_add, str):
                    value_to_add = value_to_add.strip()
                if value_to_add:
                    r.append(value_to_add)
            else:
                r.append(value_to_add)

        return r

    def _on_sub(self, internal_value, value_to_sub, **kwargs):
        """Subtract value from list.
        """
        if not isinstance(value_to_sub, self._allowed_types):
            raise TypeError("Value of the field '{}' cannot contain members of type {}, but only {}.".
                            format(self._name, type(value_to_sub), self._allowed_types))

        # Checking length
        if self._min_len is not None and len(internal_value) == self._min_len:
            raise ValueError("Value length cannot be less than {}.".format(self._min_len))

        return [v for v in internal_value if v != value_to_sub]


class UniqueList(List):
    """Unique List.
    """
    def __init__(self, name: str, **kwargs):
        """Init.
        """
        super().__init__(name, unique=True, **kwargs)


class Dict(Abstract):
    """Dictionary field.
    """
    def __init__(self, name: str, **kwargs):
        """Init.

        :param default: dict
        :param keys: tuple
        :param nonempty_keys: tuple
        """
        self._keys = kwargs.get('keys', ())
        self._nonempty_keys = kwargs.get('nonempty_keys', ())

        kwargs['default'] = kwargs.get('default', {})

        super().__init__(name, **kwargs)

    def _on_get(self, internal_value, **kwargs):
        """Get value of the field.
        """
        return _frozendict(internal_value)

    def _on_get_storable(self, internal_value, **kwargs):
        return dict(internal_value)

    def _on_set(self, value: _Union[dict, _frozendict], **kwargs):
        """Set value of the field.
        """
        if type(value) not in (dict, _frozendict):
            raise TypeError("Value of the field '{}' should be a dict. Got '{}'.".format(self._name, type(value)))

        # Internally this field stores ordinary dict
        if isinstance(value, _frozendict):
            value = dict(value)

        if self._keys:
            for k in self._keys:
                if k not in value:
                    raise ValueError("Value of the field '{}' must contain key '{}'.".format(self._name, k))

        if self._nonempty_keys:
            for k in self._nonempty_keys:
                if k not in value or value[k] is None:
                    raise ValueError("Value of the field '{}' must contain nonempty key '{}'.".format(self._name, k))

        return value

    def _on_add(self, internal_value, value_to_add: _Union[dict, _frozendict], **kwargs):
        """Add a value to the field.
        """
        if type(value_to_add) not in (dict, _frozendict):
            raise TypeError("Value of the field '{}' must be a dict.".format(self._name))

        r = dict(internal_value) if isinstance(internal_value, _frozendict) else internal_value
        r.update(value_to_add)

        return r


class Ref(Abstract):
    """Ref Field.
    """
    def __init__(self, name: str, **kwargs):
        """Init.
        """
        super().__init__(name, **kwargs)
        self._model = kwargs.get('model', '*')

    @property
    def model(self) -> str:
        return self._model

    def _on_set(self, value, **kwargs):
        """Hook.

        :type value: pytsite.odm._model.Entity | _bson_DBRef | str | None
        """
        from ._model import Entity

        # Get first item from the iterable value
        if type(value) in (list, tuple):
            value = value[0] if len(value) else None

        if isinstance(value, (_bson_DBRef, str, Entity)):
            from ._api import resolve_ref
            value = resolve_ref(value)
        else:
            raise TypeError('String, DB reference or entity expected.')

        return value

    def _on_get(self, internal_value, **kwargs):
        """Hook.
        """
        if internal_value is not None:
            from ._api import get_by_ref
            entity = get_by_ref(internal_value)
            if self._model != '*' and entity.model != self._model:
                raise TypeError("Entity of model '{}' expected.".format(self._model))
            internal_value = entity

        return internal_value

    def _on_get_jsonable(self, internal_value, **kwargs):
        """Get serializable representation of the field's value.
        """
        return '_ref:{}:{}'.format(internal_value.collection, internal_value.id) if internal_value else None


class RefsList(List):
    """List of DBRefs field.
    """
    def __init__(self, name: str, **kwargs):
        """Init.
        """
        from ._model import Entity
        self._model = kwargs.get('model', '*')

        super().__init__(name, allowed_types=(Entity,), **kwargs)

    @property
    def model(self) -> str:
        return self._model

    def _on_set(self, value, **kwargs):
        """Set value of the field.
        """
        from ._model import Entity
        if type(value) not in (list, tuple):
            raise TypeError("List or tuple expected as a value of field '{}'. Got {}.".format(self._name, repr(value)))

        # Check value
        r = []
        for item in value:
            if isinstance(item, _bson_DBRef):
                r.append(item)
            elif isinstance(item, Entity):
                r.append(item.ref)
            else:
                raise TypeError("Field '{}': list of entities or DBRefs expected. Got: {}".
                                format(self.name, repr(value)))

        return r

    def _on_get(self, internal_value, **kwargs):
        """Get value of the field.

        :rtype: _Tuple[pytsite.odm._model.Entity]
        """
        from ._api import get_by_ref

        r = []
        for dbref in internal_value:
            entity = get_by_ref(dbref)
            if entity:
                if self._model != '*' and entity.model != self._model:
                    raise TypeError("Entity of model '{}' expected.".format(self._model))
                r.append(entity)

        sort_by = kwargs.get('sort_by')
        if sort_by:
            r = sorted(r, key=lambda e: e.f_get(sort_by), reverse=kwargs.get('sort_reverse', False))

        limit = kwargs.get('limit')
        if limit is not None:
            r = r[:limit]

        return tuple(r)

    def _on_add(self, internal_value, value_to_add, **kwargs):
        """Add a value to the field.
        """
        from ._model import Entity

        if isinstance(value_to_add, Entity):
            if self._model != '*' and value_to_add.model != self._model:
                raise TypeError("Entity of model '{}' expected.".format(self._model))
        else:
            raise TypeError("Entity expected.")

        return super()._on_add(internal_value, value_to_add, **kwargs)

    def _on_sub(self, internal_value, value_to_sub, **kwargs):
        """Subtract value fom the field.
        """
        from ._model import Entity

        if isinstance(value_to_sub, Entity):
            if self._model != '*' and value_to_sub.model != self._model:
                raise TypeError("Entity of model '{}' expected.".format(self._model))
        else:
            raise TypeError("Entity expected.")

        return super()._on_sub(internal_value, value_to_sub, **kwargs)


class RefsUniqueList(RefsList):
    """Unique list of DBRefs field.
    """
    def __init__(self, name: str, **kwargs):
        """Init.
        """
        super().__init__(name, unique=True, **kwargs)


class DateTime(Abstract):
    """Datetime field.
    """
    def __init__(self, name: str, **kwargs):
        """Init.

        :param default: _datetime
        """
        kwargs['default'] = kwargs.get('default', _datetime(1970, 1, 1))

        super().__init__(name, **kwargs)

    def _on_set(self, value: _datetime, **kwargs):
        """Set field's value.
        """
        if not isinstance(value, _datetime):
            raise TypeError("DateTime expected, while got {}".format(value))

        if value.tzinfo:
            value = value.replace(tzinfo=None)

        return value

    def _on_get(self, value: _datetime, **kwargs):
        """Get field's value.
        """
        fmt = kwargs.get('fmt')
        if fmt:
            if fmt == 'ago':
                value = _lang.time_ago(value)
            elif fmt == 'pretty_date':
                value = _lang.pretty_date(value)
            elif fmt == 'pretty_date_time':
                value = _lang.pretty_date_time(value)
            else:
                value = value.strftime(fmt)

        return value

    def _on_get_jsonable(self, internal_value, **kwargs):
        return _util.w3c_datetime_str(internal_value)


class String(Abstract):
    """String field.
    """
    def __init__(self, name: str, **kwargs):
        """Init.
        """
        kwargs['default'] = kwargs.get('default', '')
        self._max_length = kwargs.get('max_length')
        self._strip_html = kwargs.get('strip_html')
        self._tidyfy_html = kwargs.get('tidyfy_html')
        self._remove_empty_html_tags = kwargs.get('remove_empty_html_tags', True)

        super().__init__(name, **kwargs)

    @property
    def max_length(self) -> int:
        """Get maximum field's length.
        """
        return self._max_length

    @max_length.setter
    def max_length(self, val: int):
        """Set maximum field's length.
        """
        self._max_length = val

    def _on_set(self, value: str, **kwargs):
        """Hook.
        """
        value = str(value).strip()

        if self._max_length is not None:
            value = value[:self._max_length]

        if value:
            if self._strip_html:
                value = _util.strip_html_tags(value)
            elif self._tidyfy_html:
                value = _util.tidyfy_html(value, self._remove_empty_html_tags)

        return value


class Integer(Abstract):
    """Integer field.
    """
    def __init__(self, name: str, **kwargs):
        """Init.
        """
        kwargs['default'] = kwargs.get('default', 0)

        super().__init__(name, **kwargs)

    def _on_set(self, value: int, **kwargs):
        """Set value of the field.
        """
        if not isinstance(value, int):
            value = int(value)

        return value

    def _on_inc(self, **kwargs):
        """Increment field's value.
        """
        return 1

    def _on_dec(self, **kwargs):
        """Increment field's value.
        """
        return 1


class Decimal(Abstract):
    """Decimal Field.
    """
    def __init__(self, name: str, **kwargs):
        """Init.

        :type precision: int
        :type round: int
        """
        self._precision = kwargs.get('precision', 28)
        self._round = kwargs.get('round')

        default = kwargs.get('default', _Decimal(0))
        if isinstance(default, float):
            default = str(default)
        if not isinstance(default, _Decimal):
            default = _Decimal(default)

        if self._round:
            default = round(default, self._round)

        kwargs['default'] = default

        super().__init__(name, **kwargs)

    def _sanitize_type(self, value) -> _Decimal:
        """Convert input value to the decimal.Decimal.

        :type value: _Decimal | float | int | str
        """
        allowed_types = (_Decimal, float, int, str)
        if type(value) not in allowed_types:
            raise TypeError("'{}' cannot be used as a value of the field '{}'.".format(repr(value), self.name))

        if isinstance(value, float):
            value = str(value)
        if not isinstance(value, _Decimal):
            value = _Decimal(value)

        if self._round:
            value = round(value, self._round)

        return value

    def _on_get_storable(self, internal_value, **kwargs):
        """Get storable value of the field.
        """
        return float(internal_value)

    def _on_set(self, value, **kwargs):
        """Set value of the field.

        :type value: _Decimal | float | int | str
        """
        return self._sanitize_type(value)

    def _on_add(self, internal_value, value_to_add, **kwargs):
        """
        :type value_to_add: _Decimal | float | integer | str
        """
        return internal_value + self._sanitize_type(value_to_add)

    def _on_sub(self, internal_value, value_to_sub, **kwargs):
        """
        :type value: _Decimal | float | integer | str
        """
        return internal_value - self._sanitize_type(value_to_sub)


class Bool(Abstract):
    """Integer field.
    """

    def __init__(self, name: str, **kwargs):
        """Init.
        """
        kwargs['default'] = kwargs.get('default', False)

        super().__init__(name, **kwargs)

    def _on_set(self, value: bool, **kwargs):
        """Set value of the field.
        """
        return bool(value)


class StringList(List):
    """List of Strings.
    """
    def __init__(self, name: str, **kwargs):
        """Init.
        """
        super().__init__(name, allowed_types=(str,), **kwargs)


class UniqueStringList(UniqueList):
    """Unique String List.
    """
    def __init__(self, name: str, **kwargs):
        """Init.
        """
        super().__init__(name, allowed_types=(str,), **kwargs)


class IntegerList(List):
    """List of Integers.
    """
    def __init__(self, name: str, **kwargs):
        """Init.
        """
        super().__init__(name, allowed_types=(int,), **kwargs)


class UniqueIntegerList(UniqueList):
    """Unique String List.
    """
    def __init__(self, name: str, **kwargs):
        """Init.
        """
        super().__init__(name, allowed_types=(int,), **kwargs)


class DecimalList(List):
    """List of Floats.
    """
    def __init__(self, name: str, **kwargs):
        """Init.
        """
        super().__init__(name, allowed_types=(float, _Decimal), **kwargs)

    def _on_set(self, value: _Iterable[_Decimal], **kwargs):
        r = []
        for item in value:
            if not isinstance(value, _Decimal):
                if isinstance(item, float):
                    item = str(item)
                item = _Decimal(item)

            r.append(item)

        return r

    def _on_add(self, value: _Decimal, **kwargs):
        if not isinstance(value, _Decimal):
            if isinstance(value, float):
                value = str(value)

            value = _Decimal(value)

        return super().add_val(value, **kwargs)

    def _on_get_storable(self, internal_value, **kwargs):
        return [float(i) for i in internal_value]


class ListList(List):
    """List of Lists.
    """
    def __init__(self, name: str, **kwargs):
        """Init.
        """
        super().__init__(name, allowed_types=(list, tuple), **kwargs)


class Virtual(Abstract):
    pass
