"""PytSite Console Options
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from typing import Any, List
from pytsite import formatters, validation, util
from . import _error


class Option:
    def __init__(self, name: str, required: bool = False, default: Any = None):
        self._name = name
        self._required = required
        self._value = None
        self._formatters = []  # type: List[formatters.Formatter]
        self._rules = []  # type: List[validation.rule.Rule]
        self._default = default

        if default is not None:
            self.value = default  # Pass default value through formatters

    @property
    def name(self) -> str:
        return self._name

    @property
    def required(self) -> bool:
        return self._required

    @property
    def signature(self) -> str:
        r = '--{}={}'.format(self._name, util.to_snake_case(self.__class__.__name__))
        if not self._required:
            r = '[{}]'.format(r)

        return r

    @property
    def value(self) -> Any:
        return self._value

    @value.setter
    def value(self, value: Any):
        for f in self._formatters:
            value = f.format(value)

        for r in self._rules:
            try:
                r.validate(value)
            except validation.error.RuleError as e:
                raise _error.Error(e)

        self._value = value


class Bool(Option):
    def __init__(self, name: str, required: bool = False, default: bool = False):
        super().__init__(name, required, default)

        self._formatters.append(formatters.Bool())

    @property
    def signature(self) -> str:
        yes = 'YES' if self._default else 'yes'
        no = 'NO' if not self._default else 'no'

        r = '--{}={}|{}'.format(self._name, yes, no)
        if not self._required:
            r = '[{}]'.format(r)

        return r


class Int(Option):
    def __init__(self, name: str, required: bool = False, default: Any = None, **kwargs):
        super().__init__(name, required, default)

        self._formatters.append(formatters.Int(minimum=kwargs.get('minimum'), maximum=kwargs.get('maximum')))


class PositiveInt(Option):
    def __init__(self, name: str, required: bool = False, default: Any = None, **kwargs):
        super().__init__(name, required, default)

        self._formatters.append(formatters.PositiveInt(maximum=kwargs.get('maximum')))


class Float(Option):
    def __init__(self, name: str, required: bool = False, default: Any = None, **kwargs):
        super().__init__(name, required, default)

        self._formatters.append(formatters.Float(minimum=kwargs.get('minimum'), maximum=kwargs.get('maximum')))


class Str(Option):
    def __init__(self, name: str, required: bool = False, default: Any = None, **kwargs):
        super().__init__(name, required, default)

        self._formatters.append(formatters.Str(max_len=kwargs.get('max_len')))
