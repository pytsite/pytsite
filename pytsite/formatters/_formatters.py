"""PytSite Formatters
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import json
from typing import Any, Union, Callable, Iterable, Type
from abc import ABC
from datetime import datetime
from pytsite import util


class Formatter(ABC):
    def __init__(self, default=None):
        self._value = default

    def set_val(self, value: Any):
        self._value = value

        return self

    def get_val(self) -> Any:
        return self._value

    def format(self, value: Any):
        return self.set_val(value).get_val()


class Transform(Formatter):
    def __init__(self, default: Any = None, transform: Union[dict, Callable[[Any], Any]] = None):
        super().__init__(default)

        if not transform:
            raise ValueError('Transformation object is not specified')

        self._transform = transform

    def set_val(self, value: Any):
        if isinstance(self._transform, dict):
            value = self._transform[value] if value in self._transform else value
        elif callable(self._transform):
            value = self._transform(value)

        return super().set_val(value)


class Bool(Formatter):
    def set_val(self, value: Any):
        return super().set_val(value in (True, 'True', 'true', 'TRUE', '1', 1, 'Y', 'y', 'Yes', 'yes', 'YES'))


class Int(Formatter):
    def __init__(self, default: int = 0, minimum: int = None, maximum: int = None):
        super().__init__(default)

        self._min = minimum
        self._max = maximum

    def set_val(self, value: Any):
        try:
            value = int(value)

            if self._min is not None and value < self._min:
                value = self._min
            if self._max is not None and value > self._max:
                value = self._max

            return super().set_val(value)

        except ValueError:
            raise ValueError('Integer expected')


class PositiveInt(Int):
    def __init__(self, default: int = 0, maximum: int = None):
        super().__init__(default, 0, maximum)


class AboveZeroInt(Int):
    def __init__(self, default: int = 1, maximum: int = None):
        super().__init__(default, 1, maximum)


class Float(Formatter):
    def __init__(self, default: float = 0.0, minimum: float = None, maximum: float = None):
        super().__init__(default)

        self._min = minimum
        self._max = maximum

    def set_val(self, value: str):
        if isinstance(value, str):
            value = value.strip()
            if not value:
                return super().set_val(None)

        try:
            value = float(value)
            if self._min is not None and value < self._min:
                value = self._min
            if self._max is not None and value > self._max:
                value = self._max

            return super().set_val(value)

        except ValueError:
            raise ValueError('Float expected')


class PositiveFloat(Float):
    def __init__(self, default: float = 0.0, maximum: float = None):
        super().__init__(default, 0.0, maximum)


class Str(Formatter):
    def __init__(self, default: str = '', max_len: int = None, min_len: int = None, lower: bool = False,
                 upper: bool = False):
        super().__init__(default)

        self._max_len = max_len
        self._min_len = min_len
        self._lower = lower
        self._upper = upper

    def set_val(self, value: str):
        value = str(value).strip()

        if self._lower:
            value = value.lower()

        if self._upper:
            value = value.upper()

        if self._min_len and len(value) < self._min_len:
            raise ValueError('Value is too short')

        if self._max_len and len(value) > self._max_len:
            value = value[:self._max_len]

        return super().set_val(value)


class Enum(Formatter):
    def __init__(self, default: Any = None, values: Iterable = None):
        super().__init__(default)

        self._values = values

    def set_val(self, value: Any):
        if value not in self._values:
            raise ValueError("Value '{}' is not acceptable".format(value))

        return super().set_val(value)


class DateTime(Formatter):
    def set_val(self, value: Any):
        if isinstance(value, str):
            value = util.parse_date_time(value)
        elif not isinstance(value, datetime):
            raise TypeError('String or datetime expected, got {}: {}'.format(type(value), value))

        return super().set_val(value)


class JSON(Formatter):
    def __init__(self, default: Any = None, allowed_types: Iterable[Type] = (object,)):
        self._allowed_types = allowed_types

        super().__init__(default)

    def set_val(self, value: Any):
        try:
            if isinstance(value, str):
                value = json.loads(value)
            if type(value) not in self._allowed_types:
                raise TypeError('{} expected, got {}'.format(self._allowed_types, type(value)))
            return super().set_val(value)
        except (json.JSONDecodeError, TypeError) as e:
            raise ValueError('Error while parsing JSON: {}'.format(e))


class JSONArray(JSON):
    def __init__(self, default: Any = None):
        super().__init__(default if default is not None else [], (list, tuple))


class JSONObject(JSON):
    def __init__(self, default: Any = None):
        super().__init__(default if default is not None else {}, (dict,))
