__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


import re
from abc import ABC, abstractmethod
from .lang import t


class Rule(ABC):
    def __init__(self, msg_id: str=None, value=None):
        """Init.
        """
        self._value = value
        self._msg_id = msg_id
        self._message = None
        self._validation_state = None

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        """Set rule's value.
        """
        self.reset()
        self._value = value

    @property
    def message(self)->str:
        """Get validation message.
        """
        if self._validation_state is None:
            raise Exception("Rule is not validated yet.")

        return self._message

    def reset(self):
        """Reset rule.
        """
        self._value = None
        self._message = None
        self._validation_state = None
        return self

    @abstractmethod
    def validate(self, validator, field_name: str)->bool:
        """Validate the rule.
        """
        pass


class NotEmptyRule(Rule):
    """Not empty rule.
    """
    def validate(self, validator, field_name: str)->bool:
        """Validate the rule.
        """
        if self._value:
            self._validation_state = True
        else:
            msg_id = self._msg_id if self._msg_id else 'pytsite.core@validation_rule_not_empty'
            self._message = t(msg_id, {'name': field_name})
            self._validation_state = False

        return self._validation_state


class IntegerRule(Rule):
    """Integer validation rule.
    """
    def validate(self, validator, field_name: str)->bool:
        """Validate the rule.
        """
        try:
            int(self._value)
            self._validation_state = True
        except ValueError:
            msg_id = self._msg_id if self._msg_id else 'pytsite.core@validation_rule_integer'
            self._message = t(msg_id, {'name': field_name})
            self._validation_state = False

        return self._validation_state


class UrlRule(Rule):
    """URL validation rule.
    """
    def validate(self, validator, field_name: str)->bool:
        """Validate the rule.
        """

        try:
            regex = re.compile(
                r'^(?:http|ftp)s?://'  # http:// or https://
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain
                r'localhost|'  # localhost...
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
                r'(?::\d+)?'  # optional port
                r'(?:/?|[/?]\S+)$', re.IGNORECASE)

            if not regex.match(str(self._value)):
                raise ValueError()

            self._validation_state = True
        except ValueError:
            msg_id = self._msg_id if self._msg_id else 'pytsite.core@validation_rule_url'
            self._message = t(msg_id, {'name': field_name})
            self._validation_state = False

        return self._validation_state


class EmailRule(Rule):
    """Email validation rule.
    """
    def validate(self, validator, field_name: str)->bool:
        """Validate the rule.
        """
        import re
        try:
            regex = re.compile('[^@]+@[^@]+\.[^@]+')
            if not regex.match(str(self._value)):
                raise ValueError()

            self._validation_state = True
        except ValueError:
            msg_id = self._msg_id if self._msg_id else 'pytsite.core@validation_rule_email'
            self._message = t(msg_id, {'name': field_name})
            self._validation_state = False

        return self._validation_state


class Validator:
    def __init__(self):
        """Init.
        """
        self._rules = {}

    def add_rule(self, field: str, rule: Rule):
        """Add a rule to the validator's field.
        """
        if field not in self._rules:
            self._rules[field] = []

        self._rules[field].append(rule)

        return self

    def has_field(self, field: str)->bool:
        """Whether the validator has a field.
        """
        return field in self._rules

    def set_value(self, field: str, value):
        """Set rule's value.
        """
        if not self.has_field(field):
            raise KeyError("Field '{0}' is not defined.". format(field))

        for rule in self._rules[field]:
            rule.value = value

        return self

    def validate(self)->bool:
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
