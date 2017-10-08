"""PytSite ODM Fields
"""
from typing import Any as _Any, Iterable as _Iterable, Union as _Union, List as _List, Optional as _Optional
from abc import ABC as _ABC
from datetime import datetime as _datetime
from decimal import Decimal as _Decimal
from copy import deepcopy as _deepcopy
from bson.dbref import DBRef as _bson_DBRef
from frozendict import frozendict as _frozendict
from pytsite import lang as _lang, util as _util, validation as _validation, formatters as _formatters
from . import _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Abstract(_ABC):
    """Base ODM Field
    """

    def __init__(self, name: str, **kwargs):
        """Init.

        :param default:
        :param required: bool
        """
        self._name = name
        self._required = kwargs.get('required', False)
        self._default = kwargs.get('default')
        self._value = self._on_set(self._default, init=True) if self._default is not None else self._default

    @property
    def required(self) -> bool:
        return self._required

    @required.setter
    def required(self, value: bool):
        self._required = value

    @property
    def is_empty(self) -> bool:
        return not bool(self._value)

    @property
    def name(self) -> str:
        """Get name of the field
        """
        return self._name

    @property
    def default(self) -> _Any:
        return self._default

    @default.setter
    def default(self, value):
        self._default = value

    def _on_get(self, value, **kwargs):
        """Hook. Transforms internal value for external representation
        """
        return value

    def get_val(self, **kwargs) -> _Any:
        """Get value of the field
        """
        value = self._on_get(self._value, **kwargs)

        return value

    def _on_get_jsonable(self, value, **kwargs):
        """Hook.
        """
        return value

    def as_jsonable(self, **kwargs) -> _Union[int, str, float, bool, dict, tuple, list]:
        """Get JSONable representation of field's value
        """
        return self._on_get_jsonable(self._value, **kwargs)

    def _on_set(self, raw_value, **kwargs):
        """Hook, called by self.set_val()
        """
        return raw_value

    def set_val(self, value, **kwargs):
        """Set value of the field
        """
        if value is None:
            self._value = _deepcopy(self._default)
        else:
            # Pass value through the hook
            self._value = self._on_set(value, **kwargs)

        return self

    def clr_val(self):
        """Reset field's value to default
        """
        return self.set_val(None)

    def _on_add(self, current_value, raw_value_to_add, **kwargs):
        """Hook, called by self.add_val()
        """
        return current_value + raw_value_to_add

    def add_val(self, value_to_add, **kwargs):
        """Add a value to the field
        """
        return self.set_val(self._on_add(self._value, value_to_add, **kwargs), **kwargs)

    def _on_sub(self, current_value, raw_value_to_sub, **kwargs):
        """Hook, called by self.sub_val()
        """
        return current_value - raw_value_to_sub

    def sub_val(self, value_to_sub, **kwargs):
        """Subtract a value from the field
        """
        return self.set_val(self._on_sub(self._value, value_to_sub, **kwargs), **kwargs)

    def _on_inc(self, **kwargs):
        """Hook, called by self.inc_val()
        """
        raise NotImplementedError("Value of the field '{}' cannot be incremented".format(self._name))

    def inc_val(self, **kwargs):
        """Increment the value of the field
        """
        return self.set_val(self._value + self._on_inc(**kwargs), **kwargs)

    def _on_dec(self, **kwargs):
        """Hook, called by self.dec_val()
        """
        raise NotImplementedError("Value of the field '{}' cannot be decremented".format(self._name))

    def dec_val(self, **kwargs):
        """Decrement the value of the field
        """
        return self.set_val(self._value - self._on_dec(**kwargs), **kwargs)

    def on_entity_delete(self):
        """Hook method to provide for fields notification mechanism about entity deletion.
        """
        pass

    def sanitize_finder_arg(self, arg):
        """Hook used for sanitizing Finder's query argument
        """
        return arg

    def __str__(self) -> str:
        """Stringify field's value
        """
        return str(self.get_val())


class Virtual(Abstract):
    """Virtual Field
    """
    pass


class List(Abstract):
    """List field
    """

    def __init__(self, name: str, **kwargs):
        """Init
        """
        self._allowed_types = kwargs.get('allowed_types', (int, str, float, list, dict, tuple))
        self._min_len = kwargs.get('min_len')
        self._max_len = kwargs.get('max_len')
        self._unique = kwargs.get('unique', False)
        self._cleanup = kwargs.get('cleanup', True)

        kwargs.setdefault('default', [])

        super().__init__(name, **kwargs)

    def _on_get(self, value, **kwargs) -> tuple:
        """Get value of the field.
        """
        return tuple(value)

    def _on_set(self, raw_value, **kwargs) -> list:
        """Set value of the field.

        :type raw_value: list | tuple
        """
        if type(raw_value) not in (list, tuple):
            raise TypeError(
                "Field '{}': list or tuple expected, got {}: {}".format(self._name, type(raw_value), raw_value))

        # Internal value is always a list
        if isinstance(raw_value, tuple):
            raw_value = list(raw_value)

        # Checking validness of types of the items
        if self._allowed_types:
            for v in raw_value:
                if not isinstance(v, self._allowed_types):
                    raise TypeError("Value of the field '{}' cannot contain members of type {}, but only {}."
                                    .format(self.name, type(v), self._allowed_types))

        # Uniquize value
        if self._unique:
            clean_val = []
            for v in raw_value:
                if v and v not in clean_val:
                    clean_val.append(v)
            raw_value = clean_val

        # Checking lengths
        if self._min_len is not None and len(raw_value) < self._min_len:
            raise ValueError("Value length cannot be less than {}.".format(self._min_len))
        if self._max_len is not None and len(raw_value) > self._max_len:
            raise ValueError("Value length cannot be more than {}.".format(self._max_len))

        # Cleaning up empty string values
        if self._cleanup:
            raw_value = _util.cleanup_list(raw_value)

        return raw_value

    def _on_add(self, current_value: list, raw_value_to_add, **kwargs) -> list:
        """Add a value to the field.
        """
        if not isinstance(raw_value_to_add, self._allowed_types):
            raise TypeError("Value of the field '{}' cannot contain members of type {}, but only {}.".
                            format(self._name, type(raw_value_to_add), self._allowed_types))

        # Checking length
        if self._max_len is not None and (len(current_value) + 1) > self._max_len:
            raise ValueError("Value length cannot be more than {}.".format(self._max_len))

        r = current_value

        # Checking for unique value
        if self._unique:
            if raw_value_to_add not in r:
                r.append(raw_value_to_add)
        else:
            if self._cleanup:
                # Cleaning up empty string values
                if isinstance(raw_value_to_add, str):
                    raw_value_to_add = raw_value_to_add.strip()
                if raw_value_to_add:
                    r.append(raw_value_to_add)
            else:
                r.append(raw_value_to_add)

        return r

    def _on_sub(self, current_value: list, raw_value_to_sub, **kwargs) -> list:
        """Subtract value from list
        """
        if not isinstance(raw_value_to_sub, self._allowed_types):
            raise TypeError("Value of the field '{}' cannot contain members of type {}, but only {}.".
                            format(self._name, type(raw_value_to_sub), self._allowed_types))

        # Checking length
        if self._min_len is not None and len(current_value) == self._min_len:
            raise ValueError("Value length cannot be less than {}.".format(self._min_len))

        return [v for v in current_value if v != raw_value_to_sub]


class UniqueList(List):
    """Unique List Field
    """

    def __init__(self, name: str, **kwargs):
        """Init.
        """
        super().__init__(name, unique=True, **kwargs)


class Dict(Abstract):
    """Dictionary Field
    """

    def __init__(self, name: str, **kwargs):
        """Init

        :param default: dict
        :param keys: tuple
        :param nonempty_keys: tuple
        """
        self._keys = kwargs.get('keys', ())  # Required keys
        self._nonempty_keys = kwargs.get('nonempty_keys', ())  # Required keys which must be non-empty
        self._dotted_keys = kwargs.get('dotted_keys', False)
        self._dotted_keys_replacement = kwargs.get('dotted_keys_replacement', ':')

        kwargs.setdefault('default', {})

        super().__init__(name, **kwargs)

    def _on_get(self, value: dict, **kwargs) -> _frozendict:
        """Hook
        """
        if self._dotted_keys:
            new_value = {}
            for k, v in value.items():
                new_value[k.replace(self._dotted_keys_replacement, '.')] = v

            value = new_value

        # Don't allow to change value outside the field's object
        return _frozendict(value)

    def _on_set(self, raw_value: _Union[dict, _frozendict], **kwargs) -> dict:
        """Hook
        """
        if type(raw_value) not in (dict, _frozendict):
            raise TypeError("Value of the field '{}' should be a dict. Got '{}'.".format(self._name, type(raw_value)))

        # Internally this field stores ordinary dict
        if isinstance(raw_value, _frozendict):
            raw_value = dict(raw_value)

        if self._dotted_keys:
            raw_value = {k.replace('.', self._dotted_keys_replacement): v for k, v in raw_value.items()}

        if self._keys:
            for k in self._keys:
                if k not in raw_value:
                    raise ValueError("Value of the field '{}' must contain key '{}'.".format(self._name, k))

        if self._nonempty_keys:
            for k in self._nonempty_keys:
                if k not in raw_value or raw_value[k] is None:
                    raise ValueError("Value of the field '{}' must contain nonempty key '{}'.".format(self._name, k))

        return raw_value

    def _on_add(self, current_value: dict, raw_value_to_add, **kwargs) -> dict:
        """Add a value to the field.
        """
        try:
            current_value.update(dict(raw_value_to_add))
        except ValueError:
            raise TypeError("Value of the field '{}' must be a dict.".format(self._name))

        return current_value


class Enum(Abstract):
    """Enumerated field
    """

    def __init__(self, name: str, **kwargs):
        """Init
        """
        self._valid_types = (int, float, str)

        self._valid_values = kwargs.get('valid_values')
        if not self._valid_values or not isinstance(self._valid_values, (list, tuple)):
            raise RuntimeError("You must specify a list of valid values for enumerated field '{}'.".format(self.name))

        for v in self._valid_values:
            if not isinstance(v, self._valid_types):
                raise TypeError("Value of argument 'valid_values' of the field '{}' should be one of these types: {}".
                                format(self.name, self._valid_types))

        super().__init__(name, **kwargs)

    def _on_set(self, raw_value, **kwargs):
        if not isinstance(raw_value, self._valid_types):
            raise TypeError("Value of the field '{}' should be one of these types: {}".
                            format(self.name, self._valid_types))

        if raw_value not in self._valid_values:
            raise ValueError(
                "Value of the field '{}' can be only one of the following: {}".format(self.name, self._valid_values))

        return raw_value

    @property
    def valid_values(self) -> tuple:
        return self._valid_values


class Ref(Abstract):
    """Reference Field
    """

    def __init__(self, name: str, **kwargs):
        """Init
        """
        self._model = kwargs.get('model', '*')
        self._ignore_missing = kwargs.get('ignore_missing', False)

        super().__init__(name, **kwargs)

    @property
    def model(self) -> str:
        return self._model

    def _on_set(self, raw_value, **kwargs) -> _Optional[_bson_DBRef]:
        """Hook

        :type raw_value: pytsite.odm.model.Entity | _bson_DBRef | str | None
        """
        # Get first item from the iterable value
        if type(raw_value) in (list, tuple):
            if len(raw_value):
                raw_value = raw_value[0]
            else:
                return None

        # Check type
        from ._model import Entity
        if not isinstance(raw_value, (_bson_DBRef, str, Entity)):
            raise TypeError("Error while setting value of the field '{}': "
                            "string, DB reference or entity expected, got '{}'.".format(self._name, repr(raw_value)))

        from ._api import resolve_ref
        ref = resolve_ref(raw_value)

        # Check entity existence
        from ._api import get_by_ref
        try:
            entity = get_by_ref(ref)
        except _error.ReferenceNotFound as e:
            if self._ignore_missing:
                return None
            raise e

        if self._model != '*' and not kwargs.get('init') and entity.model != self._model:
            raise TypeError("Only entities of model '{}' are allowed, got '{}'".format(self._model, entity.model))

        return ref

    def _on_get(self, value, **kwargs):
        """Hook

        :rtype: _Optional[Entity]
        """
        if value is None:
            return None

        from ._api import get_by_ref
        try:
            return get_by_ref(value)
        except _error.ReferenceNotFound as e:
            if self._ignore_missing:
                return None
            raise e

    def _on_get_jsonable(self, value, **kwargs):
        """Get serializable representation of the field's value.
        """
        return '_ref:{}:{}'.format(value.collection, value.id) if value else None

    def sanitize_finder_arg(self, arg):
        """Hook. Used for sanitizing Finder's query argument.
        """
        from . import _model

        if isinstance(arg, _model.Entity):
            arg = arg.ref

        elif isinstance(arg, str):
            from ._api import resolve_ref
            arg = self.sanitize_finder_arg(arg.split(',')) if ',' in arg else resolve_ref(arg)

        elif isinstance(arg, (list, tuple)):
            clean_arg = []
            for v in arg:
                clean_arg.append(self.sanitize_finder_arg(v))

            arg = clean_arg

        return arg


class RefsList(List):
    """List of References Field
    """

    def __init__(self, name: str, **kwargs):
        """Init.
        """
        from ._model import Entity
        self._model = kwargs.get('model', '*')
        self._ignore_missing = kwargs.get('ignore_missing', False)

        super().__init__(name, allowed_types=(Entity,), **kwargs)

    @property
    def model(self) -> str:
        return self._model

    def _on_set(self, raw_value, **kwargs) -> _List[_bson_DBRef]:
        """Set value of the field
        """
        from ._model import Entity
        if not isinstance(raw_value, (list, tuple)):
            raise TypeError(
                "List or tuple expected as a value of the field '{}', got '{}'".format(self._name, repr(raw_value)))

        # Check value
        r = []
        for item in raw_value:
            if isinstance(item, _bson_DBRef):
                pass
            elif isinstance(item, Entity):
                item = item.ref
            else:
                raise TypeError("Field '{}': list of entities or DBRefs expected. Got: {}".
                                format(self.name, repr(raw_value)))

            # Check model
            if self._model != '*' and not kwargs.get('init'):
                from ._api import get_by_ref

                try:
                    entity = get_by_ref(item)
                except _error.ReferenceNotFound as e:
                    if self._ignore_missing:
                        continue
                    raise e

                if entity.model != self._model:
                    raise TypeError("Only entities of model '{}' are allowed, got '{}'"
                                    .format(self._model, entity.model))

            if not self._unique or (self._unique and item not in r):
                r.append(item)

        return r

    def _on_get(self, value: _List[_bson_DBRef], **kwargs):
        """Get value of the field

        :rtype: _Tuple[pytsite.odm.model.Entity, ...]
        """
        from ._api import get_by_ref

        r = []
        for dbref in value:
            try:
                r.append(get_by_ref(dbref))
            except _error.ReferenceNotFound as exc:
                if self._ignore_missing:
                    continue
                raise exc

        sort_by = kwargs.get('sort_by')
        if sort_by:
            r = sorted(r, key=lambda e: e.f_get(sort_by), reverse=kwargs.get('sort_reverse', False))

        limit = kwargs.get('limit')
        if limit is not None:
            r = r[:limit]

        return tuple(r)

    def _on_add(self, current_value: list, raw_value_to_add, **kwargs):
        """Add a value to the field

        """
        from ._model import Entity

        if isinstance(raw_value_to_add, Entity):
            if self._model != '*' and raw_value_to_add.model != self._model:
                raise TypeError("Only entities of model '{}' are allowed, got '{}'"
                                .format(self._model, raw_value_to_add.model))
        else:
            raise TypeError("Entity expected, got '{}'".format(type(raw_value_to_add)))

        return super()._on_add(current_value, raw_value_to_add, **kwargs)

    def _on_sub(self, current_value: list, raw_value_to_sub, **kwargs):
        """Subtract value fom the field.
        """
        from ._model import Entity

        if isinstance(raw_value_to_sub, Entity):
            if self._model != '*' and raw_value_to_sub.model != self._model:
                raise TypeError("Only entities of model '{}' are allowed, got '{}'"
                                .format(self._model, raw_value_to_sub.model))
        else:
            raise TypeError("Entity expected")

        return super()._on_sub(current_value, raw_value_to_sub, **kwargs)

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
    """Unique list of DBRefs field
    """

    def __init__(self, name: str, **kwargs):
        """Init
        """
        super().__init__(name, unique=True, **kwargs)


class DateTime(Abstract):
    """Datetime Field
    """

    def __init__(self, name: str, **kwargs):
        """Init
        """
        kwargs.setdefault('default', _datetime(1970, 1, 1))

        super().__init__(name, **kwargs)

    def _on_set(self, raw_value: _Optional[_datetime], **kwargs) -> _datetime:
        """Set field's value
        """
        if not isinstance(raw_value, _datetime):
            raise TypeError("DateTime expected, got '{}'".format(type(raw_value)))

        if raw_value.tzinfo:
            raw_value = raw_value.replace(tzinfo=None)

        return raw_value

    def _on_get(self, value: _datetime, **kwargs) -> _Union[_datetime, str]:
        """Get field's value
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

    def _on_get_jsonable(self, value, **kwargs):
        return _util.w3c_datetime_str(value)


class String(Abstract):
    """String Field
    """

    def __init__(self, name: str, **kwargs):
        """Init
        """
        self._min_length = kwargs.get('min_length')
        self._max_length = kwargs.get('max_length')
        self._strip_html = kwargs.get('strip_html', False)
        self._tidyfy_html = kwargs.get('tidyfy_html', False)
        self._remove_empty_html_tags = kwargs.get('remove_empty_html_tags', True)

        kwargs.setdefault('default', '')

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

    def _on_set(self, raw_value: str, **kwargs) -> str:
        """Hook
        """
        if not isinstance(raw_value, str):
            raise TypeError("Field '{}': string object expected, got {}.".format(self.name, type(raw_value)))

        raw_value = raw_value.strip()

        if raw_value:
            # Strip HTML
            if self._strip_html:
                raw_value = _util.strip_html_tags(raw_value)

            # Tidyfy HTML
            elif self._tidyfy_html:
                raw_value = _util.tidyfy_html(raw_value, self._remove_empty_html_tags)

        # Checks lengths only value set not by constructor
        if not kwargs.get('init'):
            if self._min_length:
                v_msg_id = 'pytsite.odm@validation_field_string_min_length'
                v_msg_args = {'field': self.name}
                _validation.rule.MinLength(raw_value, v_msg_id, v_msg_args, min_length=self._min_length).validate()

            if self._max_length:
                v_msg_id = 'pytsite.odm@validation_field_string_max_length'
                v_msg_args = {'field': self.name}
                _validation.rule.MinLength(raw_value, v_msg_id, v_msg_args, max_length=self._max_length).validate()

        return raw_value


class Email(String):
    """Email String Field
    """

    def _on_set(self, raw_value: str, **kwargs) -> str:
        v_msg_id = 'pytsite.odm@validation_field_email'
        v_msg_args = {'field': self.name}

        return _validation.rule.Email(raw_value, v_msg_id, v_msg_args).validate()


class Integer(Abstract):
    """Integer Field
    """

    def __init__(self, name: str, **kwargs):
        """Init
        """
        kwargs.setdefault('default', 0)

        super().__init__(name, **kwargs)

    def _on_set(self, raw_value: int, **kwargs) -> int:
        """Set value of the field
        """
        if not isinstance(raw_value, int):
            raw_value = int(raw_value)

        return raw_value

    def _on_inc(self, **kwargs) -> int:
        """Decrement field's value hook
        """
        return 1

    def _on_dec(self, **kwargs) -> int:
        """Decrement field's value hook
        """
        return 1

    @property
    def is_empty(self) -> bool:
        # This field always is not empty
        return False

    def sanitize_finder_arg(self, arg) -> int:
        """Hook used for sanitizing Finder's query argument
        """
        return int(arg)


class Decimal(Abstract):
    """Decimal Field
    """

    def __init__(self, name: str, **kwargs):
        """Init

        :type precision: int
        :type round: int
        """
        self._precision = kwargs.get('precision', 28)
        self._round = kwargs.get('round')

        default = kwargs.get('default', 0.0)

        if self._round:
            default = round(default, self._round)

        kwargs.setdefault('default', default)

        super().__init__(name, **kwargs)

    def _on_get(self, value, **kwargs) -> _Decimal:
        """Get storable value of the field
        """
        return _Decimal(value)

    def _on_set(self, raw_value, **kwargs) -> float:
        """Set value of the field.

        :type raw_value: _Decimal | float | int | str
        """
        if not isinstance(raw_value, float):
            try:
                raw_value = float(raw_value)
            except ValueError:
                raise TypeError("'{}' cannot be used as a value of the field '{}'".format(repr(raw_value), self.name))

        if self._round:
            raw_value = round(raw_value, self._round)

        return raw_value

    def _on_add(self, current_value: float, raw_value_to_add, **kwargs) -> float:
        """
        :type raw_value_to_add: _Decimal | float | integer | str
        """
        try:
            return float(_Decimal(current_value) + _Decimal(raw_value_to_add))
        except ValueError:
            raise TypeError("'{}' cannot be used as a value of the field '{}'"
                            .format(repr(raw_value_to_add), self.name))

    def _on_sub(self, current_value, raw_value_to_sub, **kwargs) -> float:
        """
        :type value: _Decimal | float | integer | str
        """
        try:
            return float(_Decimal(current_value) - _Decimal(raw_value_to_sub))
        except ValueError:
            raise TypeError("'{}' cannot be used as a value of the field '{}'"
                            .format(repr(raw_value_to_sub), self.name))

    def sanitize_finder_arg(self, arg) -> float:
        """Hook used for sanitizing Finder's query argument
        """
        return float(arg)


class Bool(Abstract):
    """Integer Field
    """

    def __init__(self, name: str, **kwargs):
        """Init.
        """
        kwargs.setdefault('default', False)

        super().__init__(name, **kwargs)

    def _on_set(self, raw_value, **kwargs) -> bool:
        """Set value of the field.
        """
        return bool(raw_value)

    def sanitize_finder_arg(self, arg) -> bool:
        """Hook used for sanitizing Finder's query argument
        """
        return _formatters.Bool().format(arg)


class StringList(List):
    """List of Strings Field
    """

    def __init__(self, name: str, **kwargs):
        """Init.
        """
        super().__init__(name, allowed_types=(str,), **kwargs)


class UniqueStringList(UniqueList):
    """Unique String List Field
    """

    def __init__(self, name: str, **kwargs):
        """Init.
        """
        super().__init__(name, allowed_types=(str,), **kwargs)


class IntegerList(List):
    """List of Integers Field
    """

    def __init__(self, name: str, **kwargs):
        """Init.
        """
        super().__init__(name, allowed_types=(int,), **kwargs)


class UniqueIntegerList(UniqueList):
    """Unique String List Field
    """

    def __init__(self, name: str, **kwargs):
        """Init.
        """
        super().__init__(name, allowed_types=(int,), **kwargs)


class DecimalList(List):
    """List of Decimals Field
    """

    def __init__(self, name: str, **kwargs):
        """Init.
        """
        super().__init__(name, allowed_types=(float, _Decimal), **kwargs)

    def _on_set(self, raw_value: list, **kwargs) -> _List[float]:
        for i in range(0, len(raw_value)):
            raw_value[i] = float(raw_value[i]) if not isinstance(raw_value[i], float) else raw_value[i]

        return raw_value

    def _on_add(self, current_value: list, raw_value_to_add, **kwargs):
        raw_value_to_add = float(raw_value_to_add) if not isinstance(raw_value_to_add, float) else raw_value_to_add
        return super()._on_add(current_value, raw_value_to_add, **kwargs)

    def _on_sub(self, current_value: list, raw_value_to_sub, **kwargs):
        raw_value_to_sub = float(raw_value_to_sub) if not isinstance(raw_value_to_sub, float) else raw_value_to_sub
        return super()._on_sub(current_value, float(raw_value_to_sub), **kwargs)


class ListList(List):
    """List of Lists Field
    """

    def __init__(self, name: str, **kwargs):
        """Init.
        """
        super().__init__(name, allowed_types=(list, tuple), **kwargs)
