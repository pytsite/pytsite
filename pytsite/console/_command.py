"""PytSite Console Command
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from typing import Dict, Any
from abc import ABC, abstractmethod
from . import _option, _error


class Command(ABC):
    """Abstract command
    """

    def __init__(self):
        self._opts = {}  # type: Dict[str, _option.Option]
        self._args = []
        self._required_args = 0

    def define_option(self, opt: _option.Option):
        if opt.name in self._opts:
            raise KeyError("Option '{}' is already defined")

        self._opts[opt.name] = opt

    @property
    @abstractmethod
    def name(self) -> str:
        """Get name of the command.
        """
        raise NotImplementedError()

    @property
    @abstractmethod
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

    def set_opt(self, name: str, value: Any):
        try:
            if isinstance(value, bool) and isinstance(self._opts[name], _option.Str):
                value = ''

            self._opts[name].value = value
        except KeyError:
            raise _error.InvalidOption(name)

    def opt(self, name: str) -> Any:
        """Get option's value
        """
        try:
            return self._opts[name].value
        except KeyError:
            raise _error.InvalidOption(name)

    def arg(self, index: int, default: Any = None) -> Any:
        """Get argument's value
        """
        try:
            return self._args[index]
        except IndexError:
            return default

    @property
    def args(self) -> list:
        """Arguments getter
        """
        return self._args

    @args.setter
    def args(self, value: list):
        """Arguments setter
        """
        self._args = value.copy()

    def do_execute(self):
        for opt in self._opts.values():
            if opt.required and not opt.value:
                raise _error.MissingRequiredOption(opt.name)

        return self.exec()

    @abstractmethod
    def exec(self):
        """Hook.
        """
        raise NotImplementedError()
