"""ODM Fields.
"""
from typing import Any as _Any, Iterable as _Iterable, Union as _Union
from abc import ABC as _ABC
from datetime import datetime as _datetime
from decimal import Decimal as _Decimal
from bson.dbref import DBRef as _bson_DBRef
from copy import deepcopy as _deepcopy
from frozendict import frozendict as _frozendict
from pytsite import lang as _lang, util as _util, reg as _reg, logger as _logger, validation as _validation

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


_dbg = _reg.get('odm.debug.field')


class Abstract(_ABC):
    """Base field.
    """
    def __init__(self, name: str, **kwargs):
        """Init.

        :param default:
        :param required: bool
        """
        self._name = name
        self._required = kwargs.get('required', False)
        self._default = _deepcopy(kwargs.get('default'))
        self._uid = None
        self._value = None

        # Set value to default
        self.clr_val()

    @property
    def required(self) -> bool:
        return self._required

    @required.setter
    def required(self, value: bool):
        self._required = value

    @property
    def is_empty(self) -> bool:
        return not bool(self.get_val())

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
            _logger.debug("[FIELD UID CHANGED] {} -> {}".format(prev_uid, uid))

    def _on_get(self, internal_value, **kwargs):
        """Hook. Transforms internal value to external one.
        """
        return internal_value

    def get_val(self, **kwargs) -> _Any:
        """Get value of the field.
        """
        value = self._on_get(self._value, **kwargs)

        if _dbg:
            _logger.debug("[FIELD] {}.{}.get_val() -> {}".format(self._uid, self._name, repr(value)))

        return value

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
            self._value = _deepcopy(self._default)
        else:
            # Pass value through the hook
            self._value = self._on_set(value, **kwargs)

        if _dbg:
            _logger.debug("[FIELD] {}.{}.set_val({})".format(self._uid, self._name, repr(self._value)))

        return self

    def clr_val(self):
        """Reset field's value to default.
        """
        self._value = _deepcopy(self._default)

        return self

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

    def sanitize_finder_arg(self, arg):
        """Hook. Used for sanitizing Finder's query argument.
        """
        return arg

    def __str__(self) -> str:
        """Stringify field's value.
        """
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


class Enum(Abstract):
    """Enumerated field.
    """
    def __init__(self, name: str, **kwargs):
        """Init.

        :param default: dict
        :param keys: tuple
        :param nonempty_keys: tuple
        """
        super().__init__(name, **kwargs)

        self._valid_types = (int, float, str)

        self._valid_values = kwargs.get('valid_values')
        if not self._valid_values or not isinstance(self._valid_values, tuple):
            raise RuntimeError("You must specify a tuple of valid values for enumerated field '{}'.".format(self.name))

        for v in self._valid_values:
            if not isinstance(v, self._valid_types):
                raise TypeError("Value of argument 'valid_values' of the field '{}' should be one of these types: {}".
                                format(self.name, self._valid_types))

    def _on_set(self, value, **kwargs):
        if not isinstance(value, self._valid_types):
            raise TypeError("Value of the field '{}' should be one of these types: {}".
                            format(self.name, self._valid_types))

        if value not in self._valid_values:
            raise ValueError(
                "Value of the field '{}' can be only one of these: {}".format(self.name, self._valid_values))

        return value


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
            if len(value):
                value = value[0]
            else:
                return

        if isinstance(value, (_bson_DBRef, str, Entity)):
            from ._api import resolve_ref
            value = resolve_ref(value)
        else:
            raise TypeError("Error while setting value of the field '{}': "
                            "string, DB reference or entity expected, got '{}'.".format(self._name, repr(value)))

        return value

    def _on_get(self, internal_value, **kwargs):
        """Hook.
        """
        if internal_value is not None:
            from ._api import get_by_ref
            entity = get_by_ref(internal_value)
            if entity:
                if self._model != '*' and entity.model != self._model:
                    raise TypeError("Entity of model '{}' expected.".format(self._model))
                internal_value = entity
            else:
                internal_value = None

        return internal_value

    def _on_get_jsonable(self, internal_value, **kwargs):
        """Get serializable representation of the field's value.
        """
        return '_ref:{}:{}'.format(internal_value.collection, internal_value.id) if internal_value else None

    def sanitize_finder_arg(self, arg):
        """Hook. Used for sanitizing Finder's query argument.
        """
        from . import _model
        if isinstance(arg, _model.Entity):
            arg = arg.ref
        elif isinstance(arg, (list, tuple)):
            clean_arg = []
            for v in arg:
                if isinstance(v, _model.Entity):
                    clean_arg.append(v.ref)
                else:
                    clean_arg.append(v)
            arg = clean_arg

        return arg


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
                pass
            elif isinstance(item, Entity):
                item = item.ref
            else:
                raise TypeError("Field '{}': list of entities or DBRefs expected. Got: {}".
                                format(self.name, repr(value)))

            if not self._unique or (self._unique and item not in r):
                r.append(item)

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

    def sanitize_finder_arg(self, arg):
        """Hook. Used for sanitizing Finder's query argument.
        """
        from . import _model

        if not isinstance(arg, _Iterable):
            arg = (arg,)

        clean_arg = []
        for v in arg:
            if isinstance(v, _model.Entity):
                v = v.ref
            clean_arg.append(v)

        return clean_arg


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
        self._min_length = kwargs.get('min_length')
        self._max_length = kwargs.get('max_length')
        self._strip_html = kwargs.get('strip_html', False)
        self._tidyfy_html = kwargs.get('tidyfy_html', False)
        self._remove_empty_html_tags = kwargs.get('remove_empty_html_tags', True)

        super().__init__(name, **kwargs)

    @property
    def min_length(self) -> int:
        """Get minimum field's length.
        """
        return self._min_length

    @min_length.setter
    def min_length(self, val: int):
        """Set minimum field's length.
        """
        self._min_length = val

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

    @property
    def strip_html(self) -> int:
        """Get maximum field's length.
        """
        return self._strip_html

    @strip_html.setter
    def strip_html(self, val: bool):
        """Set maximum field's length.
        """
        self._strip_html = val

    @property
    def tidyfy_html(self) -> int:
        """Get maximum field's length.
        """
        return self._tidyfy_html

    @tidyfy_html.setter
    def tidyfy_html(self, val: bool):
        """Set maximum field's length.
        """
        self._tidyfy_html = val

    @property
    def remove_empty_html_tags(self) -> int:
        """Get maximum field's length.
        """
        return self._remove_empty_html_tags

    @remove_empty_html_tags.setter
    def remove_empty_html_tags(self, val: bool):
        """Set maximum field's length.
        """
        self._remove_empty_html_tags = val

    def _on_set(self, value: str, **kwargs):
        """Hook.
        """
        if not isinstance(value, str):
            raise TypeError("Field '{}': string object expected, got {}.".format(self.name, type(value)))

        value = value.strip()

        if value:
            # Strip HTML
            if self._strip_html:
                value = _util.strip_html_tags(value)

            # Tidyfy HTML
            elif self._tidyfy_html:
                value = _util.tidyfy_html(value, self._remove_empty_html_tags)

        if self._min_length:
            v_msg_id = 'pytsite.odm@validation_field_string_min_length'
            v_msg_args = {'field': self.name}
            _validation.rule.MinLength(value, v_msg_id, v_msg_args, min_length=self._min_length).validate()

        if self._max_length:
            v_msg_id = 'pytsite.odm@validation_field_string_max_length'
            v_msg_args = {'field': self.name}
            _validation.rule.MinLength(value, v_msg_id, v_msg_args, max_length=self._max_length).validate()

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

    @property
    def is_empty(self) -> bool:
        return self.get_val() is None


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
