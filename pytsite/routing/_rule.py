"""PytSite Routing Rule
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import re as _re
from typing import Type as _Type, List as _List, Union as _Union, Tuple as _Tuple
from pytsite import util as _util
from . import _error
from ._controller import Controller as _Controller, Filter as _Filter

_rule_arg_re = _re.compile('<(?:(\w+)(?:\(([\w|]*)\))?:)?(\w+)>')
_parametrized_arg_type_re = _re.compile('(\w+)\(([\w|]*)\)')


def _rule_arg_repl_func(match):
    arg_formatter = match.group(1) or 'common'
    arg_formatter_params_str = match.group(2) or ''
    arg_formatter_params = arg_formatter_params_str.split('|') if arg_formatter_params_str else []
    arg_name = match.group(3)

    if arg_formatter == 'common':
        return '(?P<{}>[^/]+)'.format(arg_name)
    elif arg_formatter == 'int':
        return '(?P<{}>\d+)'.format(arg_name)
    elif arg_formatter == 'float':
        return '(?P<{}>\d+\.\d+)'.format(arg_name)
    elif arg_formatter == 'alpha':
        return '(?P<{}>[a-z-A-Z]+)'.format(arg_name)
    elif arg_formatter == 'alnum':
        return '(?P<{}>[a-z-A-Z0-9]+)'.format(arg_name)
    elif arg_formatter == 'hex':
        return '(?P<{}>[0-9a-fA-F]+)'.format(arg_name)
    elif arg_formatter == 'choice':
        if not arg_formatter_params:
            raise _error.RuleArgumentError("Argument formatter '{}' expects parameters".format(arg_formatter))
        return '(?P<{}>({}))'.format(arg_name, '|'.join(arg_formatter_params))
    elif arg_formatter == 'path':
        return '(?P<{}>.+)'.format(arg_name)
    else:
        raise _error.RuleArgumentError('Unknown rule argument formatter: {}'.format(arg_formatter))


class Rule:
    """Routing Rule
    """

    def __init__(self, controller_class: _Type[_Controller], path: str = None, name: str = None, defaults: dict = None,
                 methods: _Union[str, _Tuple[str, ...]] = 'GET', filters: _Tuple[_Type[_Filter], ...] = None,
                 attrs: dict = None):

        if not issubclass(controller_class, _Controller):
            raise TypeError('{} expected, got {}'.format(_Controller, type(controller_class)))

        if path:
            # Cut trailing slash
            if path.endswith('/') and len(path) > 1:
                path = path[:-1]

            # Add leading slash
            if not path.startswith('/'):
                path = '/' + path

        # Sanitize methods
        if isinstance(methods, str):
            if methods == '*':
                methods = ('GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS', 'HEAD')
            else:
                methods = (methods,)
        elif not isinstance(methods, tuple):
            raise TypeError('Tuple expected, got {}'.format(type(methods)))

        # Sanitize filters
        if filters is None:
            filters = ()
        if not isinstance(filters, tuple):
            raise TypeError('Tuple expected, got {}'.format(type(filters)))
        for flt in filters:
            if not issubclass(flt, _Filter):
                raise TypeError('{} expected, got {}'.format(_Filter, type(flt)))

        self._path = path
        self._controller_class = controller_class
        self._name = name or _util.random_str()
        self._defaults = defaults.copy() if defaults else {}
        self._methods = set([m.upper() for m in methods])
        self._filters = list(filters) if filters else []
        self._attrs = attrs.copy() if attrs else {}

        # Build regular expression
        if self._path:
            rule_regex_str = _rule_arg_re.sub(_rule_arg_repl_func, path)
            self._regex = _re.compile('^/?{}/?$'.format(rule_regex_str))
            self._args = dict.fromkeys(self._regex.groupindex.keys())
        else:
            self._regex = None
            self._args = {}

        # Fill arguments with defaults
        if defaults:
            self._args.update(defaults)

    @property
    def path(self) -> str:
        return self._path

    @property
    def controller_class(self) -> _Type:
        return self._controller_class

    @property
    def name(self) -> str:
        return self._name

    @property
    def defaults(self) -> dict:
        return self._defaults

    @property
    def methods(self) -> set:
        return self._methods

    @property
    def filters(self) -> _List[_Type[_Filter]]:
        return self._filters

    @property
    def attrs(self) -> dict:
        return self._attrs

    @property
    def regex(self):
        return self._regex

    @property
    def args(self) -> dict:
        return self._args
