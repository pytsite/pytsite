"""PytSite Validator
"""
from typing import Tuple as _Tuple
from . import _rule, _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Validator:
    """PytSite Validator
    """
    def __init__(self):
        """Init.
        """
        self._rules = {}

    def add_rule(self, field: str, rule: _rule.Base):
        """Add a rule.
        """
        if field not in self._rules:
            self._rules[field] = []

        self._rules[field].append(rule)

        return self

    def has_field(self, field: str) -> bool:
        """Whether the validator has a field.
        """
        return field in self._rules

    def get_rules(self, field: str) -> _Tuple[_rule.Base]:
        """Get validator's rules.
        """
        if not self.has_field(field):
            raise KeyError("Field '{}' is not defined.".format(field))

        return tuple(self._rules[field])

    def remove_rules(self, field: str):
        """Remove all rules for the field.
        """
        if field in self._rules:
            del self._rules[field]

        return self

    def set_val(self, field: str, value):
        """Set field's value.
        """
        if not self.has_field(field):
            raise KeyError("Field '{}' is not defined.".format(field))

        # Set value of the field's rules
        for rule in self.get_rules(field):
            rule.value = value

        return self

    def validate(self):
        """Validate all the rules of the validator.
        """
        errors = {}

        # Iterate over each field
        for field_name, field_rules in self._rules.items():
            # Iterate over each rule of the field
            for rule in field_rules:
                try:
                    rule.validate()
                except _error.RuleError as e:
                    # Collect occurred errors
                    if field_name not in errors:
                        errors[field_name] = []
                    errors[field_name].append(str(e))

        # If error(s) has been occurred
        if errors:
            raise _error.ValidatorError(errors)
