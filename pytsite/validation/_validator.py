"""Validator.
"""
from . import _rule, _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Validator:
    """Validator.
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

    def get_rules(self, field: str) -> list:
        if not self.has_field(field):
            raise KeyError("Field '{}' is not defined.". format(field))

        return self._rules[field]

    def remove_rules(self, field: str):
        """Remove all rules for the field.
        """
        if field in self._rules:
            del self._rules[field]

        return self

    def set_value(self, field: str, value):
        """Set field's value.
        """
        if not self.has_field(field):
            raise KeyError("Field '{}' is not defined.". format(field))

        for rule in self._rules[field]:
            rule.value = value

        return self

    def validate(self):
        """Validate the all rules of the validator.
        """
        errors = {}

        for field_name, field_rules in self._rules.items():
            for rule in field_rules:
                try:
                    rule.validate()
                except _error.RuleError as e:
                    if field_name not in errors:
                        errors[field_name] = []
                    errors[field_name].append(str(e))
        if errors:
            raise _error.ValidatorError(errors)
