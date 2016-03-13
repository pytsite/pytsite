"""ODM Fields.
"""
from typing import Any as _Any, Iterable as _Iterable, Union as _Union, Tuple as _Tuple
from abc import ABC as _ABC
from datetime import datetime as _datetime
from decimal import Decimal as _Decimal
from bson.objectid import ObjectId as _bson_ObjectID
from bson.dbref import DBRef as _bson_DBRef
from copy import deepcopy as _deepcopy
from frozendict import frozendict as _frozendict
from pytsite import lang as _lang, util as _util

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


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
        self._modified = False
        self._default = kwargs.get('default')
        self._value = None
        """:type: _Any"""

        # Pass initial value through the setter
        self.set_val(_deepcopy(self._default))

    @property
    def nonempty(self) -> bool:
        return self._nonempty

    @property
    def name(self) -> str:
        """Get name of the field.
        """
        return self._name

    @property
    def is_modified(self) -> bool:
        """Is the field has been modified?
        """
        return self._modified

    def reset_modified(self):
        """Reset the 'modified' status of the field.
        """
        self._modified = False

        return self

    def get_val(self, **kwargs) -> _Any:
        """Get value of the field.
        """
        return self._value

    def get_storable_val(self):
        """Get value suitable to store in the database.
        """
        return self.get_val()

    def get_serializable_val(self) -> _Union[int, str, float, bool, dict, tuple, list]:
        """Get serializable representation of field's value.
        """
        return self.get_storable_val()

    def set_val(self, value, update_state: bool=True, **kwargs):
        """Set value of the field.
        """
        self._value = value
        if update_state and not self._modified:
            self._modified = True

        return self

    def clr_val(self, update_state: bool=True, **kwargs):
        """Clear the field.
        """
        self._value = _deepcopy(self._default)
        if update_state and not self._modified:
            self._modified = True

    def add_val(self, value, update_state: bool=True, **kwargs):
        """Add a value to the field.
        """
        self._value += value
        if update_state and not self._modified:
            self._modified = True

    def sub_val(self, value, update_state: bool=True, **kwargs):
        """Remove a value from the field.
        """
        self._value -= value
        if update_state and not self._modified:
            self._modified = True

    def inc_val(self, update_state: bool=True, **kwargs):
        """Increment a value of the field.
        """
        raise ArithmeticError('Value of this field cannot be incremented')

    def dec_val(self, update_state: bool=True, **kwargs):
        """Increment a value of the field.
        """
        raise ArithmeticError('Value of this field cannot be decremented')

    def on_entity_delete(self):
        """Hook method to provide for the entity notification mechanism about its deletion.
        """
        pass

    def __str__(self) -> str:
        """Stringify field's value.
        """
        return str(self._value)

    @property
    def is_empty(self) -> bool:
        return not bool(self.get_val())


class ObjectId(Abstract):
    """ObjectId field.
    """
    def set_val(self, value, update_state: bool=True, **kwargs):
        """Set value of the field.
        """
        if value is not None and not isinstance(value, _bson_ObjectID):
            raise TypeError("ObjectId expected")

        return super().set_val(value, update_state, **kwargs)

    def get_serializable_val(self):
        return str(self.get_val())

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

        if kwargs.get('default') is None:
            kwargs['default'] = ()

        super().__init__(name, **kwargs)

    def get_val(self, **kwargs) -> tuple:
        """Get value of the field.
        """
        return tuple(super().get_val(**kwargs))

    def set_val(self, value, update_state: bool=True, **kwargs):
        """Set value of the field.

        :type value: list | tuple
        """
        if not value:
            value = ()

        if type(value) not in (list, tuple):
            raise TypeError("Field '{}': list or tuple expected, but {} given.".format(self._name, repr(value)))

        # In internals value is always a list
        if isinstance(value, tuple):
            value = list(value)

        # Checking validness of types of the items
        if self._allowed_types:
            for v in value:
                if type(v) not in self._allowed_types:
                    raise TypeError("Value of the field '{}' cannot contain members of type {}."
                                    .format(self.name, type(v)))

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

        return super().set_val(value, update_state, **kwargs)

    def add_val(self, value, update_state: bool=True, **kwargs):
        """Add a value to the field.
        """
        if type(value) not in self._allowed_types:
            raise TypeError("Adding values of type '{}' is not allowed.".format(type(value)))

        # Checking length
        if self._max_len is not None and (len(self.get_val()) + 1) > self._max_len:
            raise ValueError("Value length cannot be more than {}.".format(self._max_len))

        # Checking for unique value
        if self._unique:
            if value not in self._value:
                self._value.append(value)
        else:
            if self._cleanup:
                # Cleaning up empty string values
                if isinstance(value, str):
                    value = value.strip()
                if value:
                    self._value.append(value)
            else:
                self._value.append(value)

        if update_state:
            self._modified = True

        return self

    def sub_val(self, value, update_state: bool=True, **kwargs):
        """Subtract value from list.
        """
        if type(value) not in self._allowed_types:
            raise TypeError("Subtracting values of type '{}' is not allowed.".format(type(value)))

        # Checking length
        if self._min_len is not None and len(self.get_val()) == self._min_len:
            raise ValueError("Value length cannot be less than {}.".format(self._min_len))

        self._value = [v for v in self._value if v != value]

        if update_state:
            self._modified = True

        return self


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

        default = kwargs.get('default')
        if default is None:
            kwargs['default'] = _frozendict({})
        elif not isinstance(default, _frozendict):
            kwargs['default'] = _frozendict(default)

        super().__init__(name, **kwargs)

    def get_val(self, **kwargs) -> _frozendict:
        """Get value of the field.
        """
        return super().get_val(**kwargs)

    def get_storable_val(self):
        return dict(self.get_val())

    def set_val(self, value: _Union[dict, _frozendict], update_state: bool=True, **kwargs):
        """Set value of the field.
        """
        # FIXME: workaround, I don't remember for what
        if value is None:
            return

        if type(value) not in (dict, _frozendict):
            raise TypeError("Value of the field '{}' must be a dict.".format(self._name))

        if isinstance(value, dict):
            value = _frozendict(value)

        if self._keys:
            for k in self._keys:
                if k not in value:
                    raise ValueError("Value of the field '{}' must contain key '{}'.".format(self._name, k))

        if self._nonempty_keys:
            for k in self._nonempty_keys:
                if k not in value or value[k] is None:
                    raise ValueError("Value of the field '{}' must contain nonempty key '{}'.".format(self._name, k))

        return super().set_val(value, update_state, **kwargs)

    def add_val(self, value: _Union[dict, _frozendict], update_state: bool=True, **kwargs):
        """Add a value to the field.
        """
        if type(value) not in (dict, _frozendict):
            raise TypeError("Value of the field '{}' must be a dict.".format(self._name))

        if isinstance(value, dict):
            value = _frozendict(value)

        v = dict(self.get_val())
        v.update(value)

        return self.set_val(v, update_state, **kwargs)


class Ref(Abstract):
    """Ref Field.
    """
    def __init__(self, name: str, model: str='*', **kwargs):
        """Init.
        """
        self._model = model
        super().__init__(name, **kwargs)

    @property
    def model(self) -> str:
        return self._model

    def set_val(self, value, update_state: bool=True, **kwargs):
        """Set value of the field.

        :type value: pytsite.odm._entity.Entity | _bson_DBRef | str | None
        """
        from ._entity import Entity

        if value is None:
            return super().set_val(value, update_state, **kwargs)

        # Get first item from the iterable value
        if type(value) in (list, tuple):
            value = value[0] if len(value) else None

        if isinstance(value, _bson_DBRef):
            pass
        elif isinstance(value, str):
            from ._api import resolve_ref
            value = resolve_ref(value)
        elif isinstance(value, Entity):
            # Checking if this model is allowed
            if self._model != '*' and value.model != self._model:
                raise TypeError("Instance of ODM model '{}' expected.".format(self._model))
            value = value.ref

        return super().set_val(value, update_state, **kwargs)

    def get_val(self, **kwargs):
        """Get value of the field.
        :rtype: pytsite.odm._entity.Entity | None
        """
        if isinstance(self._value, _bson_DBRef):
            from ._api import get_by_ref

            # noinspection PyTypeChecker
            referenced_entity = get_by_ref(self._value)
            if not referenced_entity:
                self.set_val(None)  # Updating field's value about missing entity

            return referenced_entity

    def get_storable_val(self):
        return self._value

    def get_serializable_val(self):
        """Get serializable representation of the field's value.
        """
        v = self.get_val()
        return '_ref:{}:{}'.format(v.ref.collection, v.ref.id) if v else None


class RefsList(List):
    """List of DBRefs field.
    """
    def __init__(self, name: str, model: str, **kwargs):
        """Init.
        """
        from ._entity import Entity
        self._model = model
        super().__init__(name, allowed_types=(_bson_DBRef, Entity), **kwargs)

    @property
    def model(self) -> str:
        return self._model

    def set_val(self, value, update_state: bool=True, **kwargs):
        """Set value of the field.
        """
        if type(value) not in (list, tuple):
            raise TypeError('List or tuple expected.')

        # Cleaning up value
        clean_value = []
        from ._entity import Entity
        for item in value:
            if isinstance(item, Entity):
                if self._model != '*' and item.model != self._model:
                    raise TypeError("Instance of ODM model '{}' expected.".format(self._model))
                clean_value.append(item.ref)
            elif isinstance(item, _bson_DBRef):
                clean_value.append(item)
            else:
                raise TypeError("Field '{}': list of DBRefs or entities expected.".format(self.name))

        return super().set_val(clean_value, update_state, **kwargs)

    def get_val(self, **kwargs):
        """Get value of the field.

        :rtype: _Tuple[pytsite.odm._entity.Entity]
        """
        from ._api import get_by_ref

        r = []
        for ref in self._value:
            entity = get_by_ref(ref)
            if entity:
                r.append(entity)

        sort_by = kwargs.get('sort_by')
        if sort_by:
            r = sorted(r, key=lambda item: item.f_get(sort_by), reverse=kwargs.get('sort_reverse', False))

        return tuple(r)

    def add_val(self, value, update_state: bool=True, **kwargs):
        """Add a value to the field.
        """
        from ._entity import Entity

        if isinstance(value, Entity):
            if self._model != '*' and value.model != self._model:
                raise TypeError("Instance of ODM model '{}' expected.".format(self._model))
            value = value.ref
        elif isinstance(value, _bson_DBRef):
            value = value
        else:
            raise TypeError("DBRef of entity expected.")

        super().add_val(value, update_state, **kwargs)

        return self

    def sub_val(self, value, update_state: bool=True, **kwargs):
        """Subtract value fom the field.
        """
        from ._entity import Entity

        if isinstance(value, Entity):
            if self._model != '*' and value.model != self._model:
                raise TypeError("Instance of ODM model '{}' expected.".format(self._model))
            value = value.ref
        elif isinstance(value, _bson_DBRef):
            pass
        else:
            raise TypeError("DBRef of entity expected.")

        super().sub_val(value, update_state, **kwargs)

        return self

    def get_storable_val(self):
        return self._value

    def get_serializable_val(self) -> list:
        return [e.serialize() for e in self.get_val()]


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
        if kwargs.get('default') is None:
            kwargs['default'] = _datetime(1970, 1, 1)

        super().__init__(name, **kwargs)

    def set_val(self, value: _datetime, update_state: bool=True, **kwargs):
        """Set field's value.
        """
        if value is None:
            value = self._default

        if not isinstance(value, _datetime):
            raise TypeError("DateTime expected, while got {}".format(value))

        if value.tzinfo:
            value = value.replace(tzinfo=None)

        return super().set_val(value, update_state, **kwargs)

    def get_val(self, fmt: str=None, **kwargs):
        """Get field's value.
        """
        value = super().get_val()  # type: _datetime

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

    def get_serializable_val(self) -> str:
        return _util.w3c_datetime_str(self.get_val())


class String(Abstract):
    """String field.
    """
    def __init__(self, name: str, **kwargs):
        """Init.
        """
        kwargs['default'] = kwargs.get('default', '')
        self._max_len = kwargs.get('max_len')

        super().__init__(name, **kwargs)

    @property
    def max_len(self) -> int:
        return self._max_len

    @max_len.setter
    def max_len(self, val: int):
        self._max_len = val

    def set_val(self, value: str, update_state: bool=True, **kwargs):
        """Set value of the field.
        """
        value = '' if value is None else str(value).strip()

        if self._max_len is not None:
            value = value[:self._max_len]

        return super().set_val(value, update_state, **kwargs)


class Integer(Abstract):
    """Integer field.
    """
    def __init__(self, name: str, **kwargs):
        """Init.
        """
        if kwargs.get('default') is None:
            kwargs['default'] = 0

        super().__init__(name, **kwargs)

    def get_val(self, **kwargs) -> int:
        return super().get_val(**kwargs)

    def set_val(self, value: int, update_state: bool=True, **kwargs):
        """Set value of the field.
        """
        if not isinstance(value, int):
            value = int(value)

        return super().set_val(int(value), update_state, **kwargs)

    def add_val(self, value: int, update_state: bool=True, **kwargs):
        """Add a value to the value of the field.
        """
        if not isinstance(value, int):
            raise ValueError('Integer expected.')
        return self.set_val(self.get_val(**kwargs) + value, update_state, **kwargs)

    def inc_val(self, update_state: bool=True, **kwargs):
        """Increment field's value.
        """
        return self.set_val(self.get_val(**kwargs) + 1, update_state, **kwargs)

    def dec_val(self, update_state: bool=True, **kwargs):
        """Increment field's value.
        """
        return self.set_val(self.get_val(**kwargs) - 1, update_state, **kwargs)


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

    def get_val(self, **kwargs) -> _Decimal:
        """Get value of the field.
        """
        return super().get_val()

    def get_storable_val(self) -> float:
        """Get storable value of the field.
        """
        return float(self.get_val())

    def set_val(self, value, update_state: bool=True, **kwargs):
        """Set value of the field.

        :type value: _Decimal | float | int | str
        """
        return super().set_val(self._sanitize_type(value), update_state, **kwargs)

    def add_val(self, value, update_state: bool=True, **kwargs):
        """
        :type value: _Decimal | float | integer | str
        """
        return super().add_val(self._sanitize_type(value), update_state, **kwargs)

    def sub_val(self, value, update_state: bool=True, **kwargs):
        """
        :type value: _Decimal | float | integer | str
        """
        return super().sub_val(self._sanitize_type(value), update_state, **kwargs)


class Bool(Abstract):
    """Integer field.
    """

    def __init__(self, name: str, **kwargs):
        """Init.
        """
        if kwargs.get('default') is None:
            kwargs['default'] = False

        super().__init__(name, **kwargs)

    def set_val(self, value: bool, update_state: bool=True, **kwargs):
        """Set value of the field.
        """
        return super().set_val(bool(value), update_state, **kwargs)


class StringList(List):
    """List of Strings.
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


class DecimalList(List):
    """List of Floats.
    """
    def __init__(self, name: str, **kwargs):
        """Init.
        """
        super().__init__(name, allowed_types=(float, _Decimal), **kwargs)

    def set_val(self, value: _Iterable[_Decimal], update_state: bool=True, **kwargs):
        if type(value) in (list, tuple):
            clean_val = []
            for item in value:
                if not isinstance(value, _Decimal):
                    if isinstance(item, float):
                        item = str(item)
                    item = _Decimal(item)

                clean_val.append(item)

            value = clean_val

        return super().set_val(value, update_state, **kwargs)

    def add_val(self, value: _Decimal, update_state: bool=True, **kwargs):
        if not isinstance(value, _Decimal):
            if isinstance(value, float):
                value = str(value)

            value = _Decimal(value)

        return super().add_val(value, update_state, **kwargs)

    def get_storable_val(self) -> _Iterable[float]:
        return [float(i) for i in self.get_val()]


class ListList(List):
    """List of Lists.
    """
    def __init__(self, name: str, **kwargs):
        """Init.
        """
        super().__init__(name, allowed_types=(list, tuple), **kwargs)


class Virtual(Abstract):
    pass
