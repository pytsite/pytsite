"""PytSite Routing Rule Map.
"""
import re as _re
from typing import Dict as _Dict
from . import _rule, _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_rule_arg_re = _re.compile('<([\w\-]+)>')


class RuleMap:
    def __init__(self):
        self._rules = {}  # type: _Dict[str, _rule.Rule]

    def add(self, rule: _rule.Rule):
        if rule.name in self._rules:
            raise _error.RuleExists("Rule with name '{}' is already added".format(rule.name))

        self._rules[rule.name] = rule

    def get(self, name: str):
        """Get rule by name.
        """
        if name not in self._rules:
            raise _error.RuleNotFound("Rule with name '{}' is not found".format(name))

        return self._rules[name]

    def match(self, path: str, method: str = 'GET') -> _rule.Rule:
        for rule in self._rules.values():
            m = rule.regex.match(path)
            if not m or rule.method != method.upper():
                continue

            rule.arg_values = m.groups()

            return rule

        raise _error.RuleNotFound("No rules match path '{}'".format(path))

    def path(self, name: str, args: dict = None) -> str:
        """Build path for a rule.
        """
        def repl(match):
            nonlocal rule

            arg_k = match.group(1)

            if arg_k in args:
                return args.pop(arg_k)
            elif arg_k in rule.defaults:
                return rule.defaults[arg_k]
            else:
                raise _error.RulePathBuildError("Argument '{}' for rule '{}' is not provided".format(arg_k, name))

        if args is None:
            args = {}

        rule = self.get(name)
        path = _rule_arg_re.sub(repl, rule.path)

        # Add remaining args as query string
        if args:
            path += '?' + '&'.join(['{}={}'.format(k, v) for k, v in args.items()])

        return path
