"""PytSite Routing Rule Map.
"""
import re as _re
from typing import Dict as _Dict, Hashable as _Hashable
from . import _rule, _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_rule_arg_re = _re.compile('<((\w+:)?[\w\-]+)>')
_rule_arg_param_re = _re.compile('\w+:')


class RulesMap:
    def __init__(self):
        self._rules_by_method_path = {}  # type: _Dict[_Hashable, _rule.Rule]
        self._rules_by_name = {}  # type: _Dict[_Hashable, _rule.Rule]

    def add(self, rule: _rule.Rule):
        rule_k = (rule.method if rule.method != '*' else 'ANY', rule.path)

        # Check if the rule with same pattern but for all methods has been added already
        if rule_k[0] != 'ANY' and ('ANY', rule_k) in self._rules_by_method_path:
            raise _error.RuleExists("Rule '{}' is already added".format(rule_k))

        if rule_k in self._rules_by_method_path:
            raise _error.RuleExists("Rule '{}' is already added".format(rule_k))

        self._rules_by_method_path[rule_k] = rule
        self._rules_by_name[rule.name] = rule

    def get(self, name: str):
        """Get rule by name.
        """
        try:
            return self._rules_by_name[name]
        except KeyError:
            raise _error.RuleNotFound("Rule with name '{}' is not found".format(name))

    def match(self, path: str, method: str = 'GET') -> _rule.Rule:
        if not path.startswith('/'):
            path = '/' + path

        for rule in self._rules_by_name.values():
            m = rule.regex.match(path)
            if not m or rule.method not in (method.upper(), '*'):
                continue

            # Fill rule's arguments
            for group_n, group_i in rule.regex.groupindex.items():
                rule.args[group_n] = m.group(group_n)

            return rule

        raise _error.RuleNotFound("No rules match path '{}'".format(path))

    def path(self, name: str, args: dict = None) -> str:
        """Build path for a rule.
        """
        def repl(match):
            nonlocal rule

            arg_k = _rule_arg_param_re.sub('', match.group(1))

            if arg_k in args:
                return str(args.pop(arg_k))
            elif arg_k in rule.defaults:
                return str(rule.defaults[arg_k])
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
