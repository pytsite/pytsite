"""PytSite Routing Rule.
"""
import re as _re
from pytsite import util as _util

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_remove_slashes_re = _re.compile('(^/+|/+$)')
_rule_arg_re = _re.compile('<([\w\-:]+)>')


def _rule_arg_repl(match):
    arg_t = 'common'
    arg = match.group(1).split(':')
    if len(arg) > 1:
        arg_t = arg[0]

    if arg_t == 'common':
        return '([^/]+)'
    elif arg_t == 'int':
        return '(\d+)'
    elif arg_t == 'hex':
        return '([0-9a-fA-F]+)'
    elif arg_t == 'path':
        return '(.+)'
    else:
        raise RuntimeError('Unknown argument type: {}'.format(arg_t))


class Rule:
    def __init__(self, path: str, handler, name: str = None, defaults: dict = None, method: str = 'GET',
                 attrs: dict = None):
        if not callable(handler):
            raise RuntimeError("HTTP API handler for '{}' is not callable".format(path))

        if not name:
            name = _util.random_str()

        # Remove leading and trailing slashes
        path = _remove_slashes_re.sub('', path)

        self._path = path
        self._handler = handler
        self._name = name
        self._defaults = defaults if defaults else {}
        self._method = method.upper()
        self._attrs = attrs if attrs else {}
        self._arg_names = [_re.sub('\w+:', '', r) for r in _rule_arg_re.findall(path)]
        self._arg_values = []

        rule_regex = _rule_arg_re.sub(_rule_arg_repl, path)
        self._regex = _re.compile('^{}$'.format(rule_regex))

    @property
    def path(self) -> str:
        return self._path

    @property
    def handler(self):
        return self._handler

    @property
    def name(self) -> str:
        return self._name

    @property
    def defaults(self) -> str:
        return self._defaults

    @property
    def method(self) -> str:
        return self._method

    @property
    def attrs(self) -> dict:
        return self._attrs

    @property
    def regex(self):
        return self._regex

    @property
    def arg_names(self) -> list:
        return self._arg_names

    @property
    def arg_values(self) -> list:
        return self._arg_values

    @arg_values.setter
    def arg_values(self, value: list):
        self._arg_values = value

    @property
    def args(self) -> dict:
        return dict(zip(self._arg_names, self._arg_values))
