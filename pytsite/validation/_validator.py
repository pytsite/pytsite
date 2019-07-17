"""PytSite Validator
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from typing import Tuple, List, Dict
from ._rule import Rule
from ._error import ValidatorError, RuleError


class Validator:
    """PytSite Validator
    """

    def __init__(self):
        """Init
        """
        self._rules = {}  # type: Dict[str, List[]]

    def add_rule(self, field: str, rule: Rule):
        """Add a rule.
        """
        if field not in self._rules:
            self._rules[field] = []

        self._rules[field].append(rule)

        return self

    def has_field(self, field: str) -> bool:
        """Whether the validator has a field
        """
        return field in self._rules

    def get_rules(self, field: str) -> Tuple[Rule]:
        """Get validator's rules
        """
        if not self.has_field(field):
            raise KeyError("Field '{}' is not defined".format(field))

        return tuple(self._rules[field])

    def remove_rules(self, field: str):
        """Remove all rules for the field
        """
        if field in self._rules:
            del self._rules[field]

        return self

    def set_val(self, field: str, value):
        """Set field's value.
        """
        if not self.has_field(field):
            raise KeyError("Field '{}' is not defined".format(field))

        # Set value of the field's rules
        for rule in self.get_rules(field):
            rule.value = value

        return self

    def validate(self, fields: List[str] = None):
        """Validate rules
        """
        errors = {}

        if fields is None:
            rules = {name: rule for name, rule in self._rules.items() if name in fields}
        else:
            rules = self._rules

        # Each rules list
        for field_name, field_rules in rules.items():
            # Each rule
            for rule in field_rules:
                try:
                    rule.validate()
                except RuleError as e:
                    # Collect occurred errors
                    if field_name not in errors:
                        errors[field_name] = []
                    errors[field_name].append(str(e))

        if errors:
            raise ValidatorError(errors)
