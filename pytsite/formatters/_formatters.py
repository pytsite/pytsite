"""PytSite Router Formatters
"""
import json as _json
from typing import Any as _Any
from abc import ABC as _ABC
from datetime import datetime as _datetime
from pytsite import util as _util

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Formatter(_ABC):
    def __init__(self):
        self._value = None

    def set_val(self, value: _Any):
        self._value = value

        return self

    def get_val(self) -> _Any:
        return self._value

    def format(self, value: _Any):
        return self.set_val(value).get_val()


class Bool(Formatter):
    def set_val(self, value: _Any):
        true = (True, 'True', 'true', 'TRUE', '1', 1, 'Y', 'y', 'Yes', 'yes', 'YES')

        return super().set_val(True if value in true else False)


class Int(Formatter):
    def __init__(self, minimum: int = None, maximum: int = None):
        super().__init__()
        self._min = minimum
        self._max = maximum

    def set_val(self, value: str):
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
    def __init__(self, maximum: int = None):
        super().__init__(0, maximum)


class Float(Formatter):
    def __init__(self, minimum: float = None, maximum: float = None):
        super().__init__()
        self._min = minimum
        self._max = maximum

    def set_val(self, value: str):
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
    def __init__(self, maximum: float = None):
        super().__init__(0.0, maximum)


class Str(Formatter):
    def __init__(self, max_len: int = None):
        super().__init__()
        self._max_len = max_len

    def set_val(self, value: str):
        value = str(value).strip()
        if self._max_len is not None and len(value) > self._max_len:
            value = value[:self._max_len]

        return super().set_val(value)


class DateTime(Formatter):
    def set_val(self, value: _Any):
        if isinstance(value, str):
            try:
                value = _util.parse_w3c_datetime_str(value)
            except ValueError:
                value = _util.parse_rfc822_datetime_str(value)
        elif not isinstance(value, _datetime):
            raise TypeError('String or datetime expected, got {}: {}'.format(type(value), value))

        return super().set_val(value)


class JSON(Formatter):
    def set_val(self, value: str):
        try:
            return super().set_val(_json.loads(value))
        except (_json.JSONDecodeError, TypeError) as e:
            raise ValueError('Error while parsing JSON: {}'.format(e))


class JSONArrayToList(JSON):
    def set_val(self, value: str):
        super().set_val(value)

        if not isinstance(self._value, list):
            raise ValueError('Should be a JSON array')

        return self


class JSONArrayToTuple(JSONArrayToList):
    def set_val(self, value: str):
        super().set_val(value)

        self._value = tuple(self._value)

        return self


class JSONObjectToDict(JSON):
    def set_val(self, value: str):
        super().set_val(value)

        if not isinstance(self._value, dict):
            raise ValueError('Should be a JSON object')

        return self
