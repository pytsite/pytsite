"""PytSite Routing Rule.
"""
import re as _re
from pytsite import util as _util

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_sanitize_slashes_re = _re.compile('(/+$)')
_rule_arg_re = _re.compile('<([\w\-:]+)>')


def _rule_arg_repl(match):
    arg_type = 'common'
    arg = match.group(1).split(':')
    if len(arg) > 1:
        arg_type = arg[0]
        arg_name = arg[1]
    else:
        arg_name = arg[0]

    if arg_type == 'common':
        return '(?P<{}>[^/]+)'.format(arg_name)
    elif arg_type == 'int':
        return '(?P<{}>\d+)'.format(arg_name)
    elif arg_type == 'hex':
        return '(?P<{}>[0-9a-fA-F]+)'.format(arg_name)
    elif arg_type == 'path':
        return '(?P<{}>.+)'.format(arg_name)
    else:
        raise RuntimeError('Unknown argument type: {}'.format(arg_type))


class Rule:
    def __init__(self, path: str, handler, name: str = None, defaults: dict = None, method: str = 'GET',
                 attrs: dict = None):
        if not (isinstance(handler, str) or callable(handler)):
            raise RuntimeError("Handler of path '{}' should be either a callable or a str".format(path))

        if not name:
            name = _util.random_str()

        # Remove leading and trailing slashes
        if path != '/':
            path = _sanitize_slashes_re.sub('', path)
            if not path.startswith('/'):
                path = '/' + path

        self._path = path
        self._handler = handler
        self._name = name
        self._method = method.upper()
        self._attrs = attrs if attrs else {}

        # Build regular expression
        rule_regex_str = _rule_arg_re.sub(_rule_arg_repl, path)
        self._regex = _re.compile('^{}$'.format(rule_regex_str))

        # Build arguments dictionary based on regular expression
        self._args = dict.fromkeys(self._regex.groupindex.keys())

        # Fill arguments with defaults
        if defaults:
            self._args.update(defaults)

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
    def method(self) -> str:
        return self._method

    @property
    def attrs(self) -> dict:
        return self._attrs

    @property
    def regex(self):
        return self._regex

    @property
    def args(self) -> dict:
        return self._args
