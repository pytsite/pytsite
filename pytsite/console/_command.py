"""Console Commands
"""
from typing import Dict as _Dict, List as _List, Any as _Any
from abc import ABC as _ABC, abstractmethod as _abstractmethod
from . import _option, _argument, _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Command(_ABC):
    """Abstract command.
    """

    def __init__(self):
        self._options = {}  # type: _Dict[str, _option.Option]
        self._arguments = []  # type: _List[_argument.Argument]
        self._required_args = 0

    def _define_option(self, opt: _option.Option):
        if opt.name in self._options:
            raise KeyError("Option '{}' is already defined")

        self._options[opt.name] = opt

    def _define_argument(self, arg: _argument.Argument):
        if arg.required:
            if self._arguments and not self._arguments[-1].required:
                raise RuntimeError('Required arguments cannot be defined after non-required ones')

            self._required_args += 1

        self._arguments.append(arg)

    @property
    @_abstractmethod
    def name(self) -> str:
        """Get name of the command.
        """
        raise NotImplementedError()

    @property
    @_abstractmethod
    def description(self) -> str:
        """Get description of the command.
        """
        raise NotImplementedError()

    @property
    def signature(self) -> str:
        """Get signature of the command.
        """
        options_sig = ' '.join([opt.signature for opt in self._options.values()])
        arguments_sig = ' '.join([arg.signature for arg in self._arguments])

        return '{} {} {}'.format(self.name, options_sig, arguments_sig)

    def set_option_value(self, name: str, value: _Any):
        try:
            if isinstance(value, bool) and isinstance(self._options[name], _option.Str):
                value = ''

            self._options[name].value = value
        except KeyError:
            raise _error.InvalidOption(name)

    def get_option_value(self, name: str) -> _Any:
        try:
            return self._options[name].value
        except KeyError:
            raise _error.InvalidOption(name)

    def set_argument_value(self, index: int, value: str):
        max_args = len(self._arguments)

        if not max_args or (index + 1) > max_args:
            raise _error.TooManyArguments()

        self._arguments[index].value = value

    def get_argument_value(self, index: int) -> _Any:
        try:
            return self._arguments[index].value
        except KeyError:
            raise KeyError('Argument index {} is too large'.format(index))

    def do_execute(self):
        for opt in self._options.values():
            if opt.required and not opt.value:
                raise _error.MissingRequiredOption(opt.name)

        for arg in self._arguments:
            if arg.required and not arg.value:
                raise _error.MissingRequiredArgument(arg.name)

        return self.execute()

    @_abstractmethod
    def execute(self):
        """Hook.
        """
        raise NotImplementedError()
