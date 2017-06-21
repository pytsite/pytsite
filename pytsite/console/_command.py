"""Console Commands
"""
from typing import Dict as _Dict, Any as _Any
from abc import ABC as _ABC, abstractmethod as _abstractmethod
from . import _option, _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Command(_ABC):
    """Abstract command.
    """

    def __init__(self):
        self._opts = {}  # type: _Dict[str, _option.Option]
        self._args = []
        self._required_args = 0

    def define_option(self, opt: _option.Option):
        if opt.name in self._opts:
            raise KeyError("Option '{}' is already defined")

        self._opts[opt.name] = opt

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
        options_sig = ' '.join([opt.signature for opt in self._opts.values()])
        if options_sig:
            options_sig = ' ' + options_sig

        return '{}{}'.format(self.name, options_sig)

    def set_opt(self, name: str, value: _Any):
        try:
            if isinstance(value, bool) and isinstance(self._opts[name], _option.Str):
                value = ''

            self._opts[name].value = value
        except KeyError:
            raise _error.InvalidOption(name)

    def opt(self, name: str) -> _Any:
        """Get option's value
        """
        try:
            return self._opts[name].value
        except KeyError:
            raise _error.InvalidOption(name)

    def set_args(self, args: list):
        self._args = args.copy()

    def arg(self, index: int) -> _Any:
        """Get argument's value
        """
        try:
            return self._args[index]
        except IndexError:
            raise _error.MissingArgument(arg_index=index)

    @property
    def args(self) -> list:
        """Get all arguments
        """
        return self._args.copy()

    def do_execute(self):
        for opt in self._opts.values():
            if opt.required and not opt.value:
                raise _error.MissingRequiredOption(opt.name)

        return self.exec()

    @_abstractmethod
    def exec(self):
        """Hook.
        """
        raise NotImplementedError()
