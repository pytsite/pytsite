"""PytSite Routing Controller
"""

from typing import List as _List, Dict as _Dict, Any as _Any
from abc import ABC as _ABC, abstractmethod as _abstractmethod
from pytsite import formatter as _formatter, validation as _validation, http as _http

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Controller(_ABC):
    def __init__(self):
        """Init.
        """
        self._formatters = {}  # type: _Dict[str, _List[_formatter.Formatter]]
        self._rules = {}  # type: _Dict[str, _List[_validation.rule.Rule]]
        self._args = {}

        self._setup()

    def _setup(self):
        """Hook.
        """
        pass

    def add_formatter(self, name: str, formatter: _formatter.Formatter):
        """Add a formatter.
        """
        if name not in self._formatters:
            self._formatters[name] = []

        self._formatters[name].append(formatter)

    def add_rule(self, name: str, r: _validation.rule.Rule):
        """Add a validation rule.
        """
        if name not in self._rules:
            self._rules[name] = []

        self._rules[name].append(r)

    def _process_input(self, internal_dict: _Dict, value: _Dict):
        for k, v in value.items():
            internal_dict[k] = v
            if k in self._formatters:
                for f in self._formatters[k]:
                    internal_dict[k] = f.format(internal_dict[k])
            if k in self._rules:
                for r in self._rules[k]:
                    try:
                        r.validate(internal_dict[k])
                    except _validation.error.RuleError as e:
                        raise _validation.error.RuleError('pytsite.router@input_validation_error', {
                            'field_name': k,
                            'error': str(e),
                        })

    def arg(self, name: str, default: _Any = None):
        return self._args.get(name, default)

    def arg_set(self, name: str, value: _Any):
        self._args[name] = value

    @staticmethod
    def redirect(location: str, status: int = 302) -> _http.response.Redirect:
        return _http.response.Redirect(location, status)

    @staticmethod
    def not_found(description: str = None, response: _http.response.Response = None):
        return _http.error.NotFound(description, response)

    @staticmethod
    def unauthorized(description: str = None, response: _http.response.Response = None):
        return _http.error.Unauthorized(description, response)

    @staticmethod
    def forbidden(description: str = None, response: _http.response.Response = None):
        return _http.error.Forbidden(description, response)

    @staticmethod
    def server_error(description: str = None, response: _http.response.Response = None):
        return _http.error.InternalServerError(description, response)

    @property
    def args(self) -> _Dict:
        return self._args

    @args.setter
    def args(self, value: _Dict):
        self._process_input(self._args, value)

    @_abstractmethod
    def exec(self):
        pass
