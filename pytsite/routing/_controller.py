"""PytSite Routing Controller
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import magic
from typing import List, Dict, Any, Union, Mapping
from abc import ABC as _ABC, abstractmethod
from os import path as p_path
from mimetypes import guess_extension
from pytsite import formatters, validation, http, util


class ControllerArgs(dict):
    def __init__(self, **kwargs):
        """Init
        """
        super().__init__()

        self._formatters = kwargs.get('formatters', {})  # type: Dict[str, List[formatters.Formatter]]
        self._rules = kwargs.get('rules', {})  # type: Dict[str, List[validation.rule.Rule]]

    def add_formatter(self, key: str, formatter: formatters.Formatter, use_default: bool = True):
        """Add a formatter of the field
        """
        if key not in self._formatters:
            self._formatters[key] = []

        self._formatters[key].append(formatter)

        # Set arg's default value from formatter's default one
        if use_default:
            self[key] = formatter.get_val()

    def rm_formatter(self, key: str):
        """Remove a formatter of the field
        """
        if key in self._formatters:
            del self._formatters[key]

    def add_validation(self, key: str, rule: validation.rule.Rule):
        """Add a validation rule of the field
        """
        if key not in self._rules:
            self._rules[key] = []

        self._rules[key].append(rule)

    def rm_validation(self, key: str):
        """Remove a validation rule of the field
        """
        if key in self._rules:
            del self._rules[key]

    def update(self, other: Mapping, **kwargs):
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
                except validation.error.RuleError as e:
                    raise validation.error.RuleError('pytsite.router@input_validation_error', {
                        'field_name': k,
                        'error': str(e),
                    })

    def __setitem__(self, key: str, value: Any):
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
        self._response = None

    @staticmethod
    def redirect(location: str, status: int = 302) -> http.RedirectResponse:
        """Return a redirect
        """
        return http.RedirectResponse(location, status)

    def file(self, path: str, name: str = None, mime: str = None, mode: str = 'rb'):
        """Return a file stream response
        """
        try:
            if not name:
                name = p_path.basename(path)

            if not mime:
                mime = magic.from_file(path, True)

            if not p_path.splitext(name)[1] and mime:
                name += guess_extension(mime)

            headers = {'Content-Disposition': 'attachment; filename="{}"'.format(util.url_quote(name))}

            return http.Response(open(path, mode), 200, headers, mime, direct_passthrough=True)

        except FileNotFoundError:
            return self.not_found()

    @staticmethod
    def warning(description: Union[str, Exception] = None, code: int = 500):
        """Raise a 'UserWarning' exception
        """
        return UserWarning(description, code)

    @staticmethod
    def not_found(description: Union[str, Exception] = None, response: http.Response = None):
        """Raise a 'Not found' exception
        """
        return http.error.NotFound(description, response)

    @staticmethod
    def unauthorized(description: Union[str, Exception] = None, response: http.Response = None):
        """Raise an 'Unauthorized' exception
        """
        return http.error.Unauthorized(description, response)

    @staticmethod
    def forbidden(description: Union[str, Exception] = None, response: http.Response = None):
        """Raise a 'Forbidden' exception
        """
        return http.error.Forbidden(description, response)

    @staticmethod
    def server_error(description: Union[str, Exception] = None, response: http.Response = None):
        """Raise an 'Internal server error' exception
        """
        return http.error.InternalServerError(description, response)

    @property
    def args(self) -> ControllerArgs:
        """Arguments getter
        """
        return self._args

    def arg(self, name: str, default: Any = None) -> Any:
        """Shortcut to get argument's value without KeyError raising
        """
        return self._args.get(name, default)

    @property
    def request(self) -> http.Request:
        """Current request object getter
        """
        if not self._request:
            raise RuntimeError('Request is not set yet')

        return self._request

    @request.setter
    def request(self, request: http.Request):
        """Current request object setter
        """
        self._request = request

    @property
    def response(self) -> http.Response:
        """Current response object getter
        """
        if not self._response:
            raise RuntimeError('Response is not set yet')

        return self._response

    @response.setter
    def response(self, response: http.Response):
        """Current response object setter
        """
        self._response = response

    @abstractmethod
    def exec(self):
        """Execute the controller
        """
        pass


class Filter(Controller):
    def exec(self):
        """Execute the controller
        """
        raise NotImplementedError('This method must be implemented by filter controllers')

    def before(self):
        """Hook to call before request processing
        """
        pass

    def after(self):
        """Hook to call after request processing
        """
        pass
