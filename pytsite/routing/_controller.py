"""PytSite Routing Base Controller
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from typing import List as _List, Dict as _Dict, Any as _Any, Union as _Union, Mapping as _Mapping
from abc import ABC as _ABC, abstractmethod as _abstractmethod
from pytsite import formatters as _formatter, validation as _validation, http as _http


class ControllerArgs(dict):
    def __init__(self, seq=None, **kwargs):
        """Init
        """
        super().__init__(seq or {}, **kwargs)

        self._formatters = kwargs.get('formatters', {})  # type: _Dict[str, _List[_formatter.Formatter]]
        self._rules = kwargs.get('rules', {})  # type: _Dict[str, _List[_validation.rule.Rule]]

    def add_formatter(self, key: str, formatter: _formatter.Formatter):
        """Add a formatter for the field
        """
        if key not in self._formatters:
            self._formatters[key] = []

        self._formatters[key].append(formatter)

    def add_validation(self, key: str, rule: _validation.rule.Rule):
        """Add a validation rule
        """
        if key not in self._rules:
            self._rules[key] = []

        self._rules[key].append(rule)

    def update(self, other: _Mapping, **kwargs):
        """It is important to pass all values through formatters
        """
        for k, v in other.items():
            self[k] = v

        for k, v in kwargs.items():
            self[k] = v

    def validate(self):
        """Validate values
        """
        for k, v in self.items():
            if k not in self._rules:
                continue

            for r in self._rules[k]:
                try:
                    r.validate(v)
                except _validation.error.RuleError as e:
                    raise _validation.error.RuleError('pytsite.router@input_validation_error', {
                        'field_name': k,
                        'error': str(e),
                    })

    def __setitem__(self, key: str, value: _Any):
        # Apply formatters
        if key in self._formatters:
            for f in self._formatters[key]:
                try:
                    value = f.format(value)
                except ValueError as e:
                    raise ValueError("Field '{}' cannot be properly formatted: {}".format(key, e))

        super().__setitem__(key, value)


class Controller(_ABC):
    """PytSite Routing Base Controller
    """

    def __init__(self):
        """Init
        """
        self._args = ControllerArgs()
        self._files = {}
        self._request = None

    @staticmethod
    def redirect(location: str, status: int = 302) -> _http.RedirectResponse:
        """Return a redirect
        """
        return _http.RedirectResponse(location, status)

    @staticmethod
    def not_found(description: _Union[str, Exception] = None, response: _http.Response = None):
        """Return a 'Not found' exception
        """
        return _http.error.NotFound(description, response)

    @staticmethod
    def unauthorized(description: _Union[str, Exception] = None, response: _http.Response = None):
        """Return an 'Unauthorized' exception
        """
        return _http.error.Unauthorized(description, response)

    @staticmethod
    def forbidden(description: _Union[str, Exception] = None, response: _http.Response = None):
        """Return a 'Forbidden' exception
        """
        return _http.error.Forbidden(description, response)

    @staticmethod
    def server_error(description: _Union[str, Exception] = None, response: _http.Response = None):
        """Return an 'Internal server error' exception
        """
        return _http.error.InternalServerError(description, response)

    @property
    def args(self) -> ControllerArgs:
        """Arguments getter
        """
        return self._args

    def arg(self, name: str, default: _Any = None) -> _Any:
        """Shortcut to get argument's value without KeyError raising
        """
        return self._args.get(name, default)

    @property
    def request(self) -> _http.Request:
        """Current request object getter
        """
        if not self._request:
            raise RuntimeError('Request is not set yet')

        return self._request

    @request.setter
    def request(self, request: _http.Request):
        """Current request object setter
        """
        self._request = request

    @_abstractmethod
    def exec(self):
        """Execute the controller
        """
        pass
