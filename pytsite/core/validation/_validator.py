"""Validator.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from . import _rule


class Validator:
    """Validator.
    """
    def __init__(self):
        """Init.
        """
        self._rules = {}

    def add_rule(self, field: str, rule: _rule.Base):
        """Add a rule to the validator field.
        """
        if field not in self._rules:
            self._rules[field] = []

        self._rules[field].append(rule)

        return self

    def has_field(self, field: str) -> bool:
        """Whether the validator has a field.
        """
        return field in self._rules

    def remove_rules(self, field: str):
        """Remove all rules for the field.
        """
        if field in self._rules:
            del self._rules[field]

        return self

    def set_value(self, field: str, value):
        """Set rule's value.
        """
        if not self.has_field(field):
            raise KeyError("Field '{}' is not defined.". format(field))

        for rule in self._rules[field]:
            rule.value = value

        return self

    def validate(self) -> bool:
        """Validate the validator.
        """
        r = True
        for field_name, rules in self._rules.items():
            for rule in rules:
                if not rule.validate(self, field_name) and r is True:
                    r = False
        return r

    @property
    def messages(self):
        """Get validation messages.
        """
        r = {}
        for field_name, rules in self._rules.items():
            for rule in rules:
                msg = rule.message
                if msg:
                    if field_name not in r:
                        r[field_name] = []
                    r[field_name].append(rule.message)

        return r
