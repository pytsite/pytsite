"""Basic Validation Rules.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import re
from abc import ABC, abstractmethod
from pytsite.core.lang import t


class BaseRule(ABC):
    """Base Rule.
    """

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
    def validate(self, validator=None, field_name: str=None) -> bool:
        """Validate the rule.
        """
        raise NotImplementedError()


class NotEmptyRule(BaseRule):
    """Not empty rule.
    """

    def validate(self, validator=None, field_name: str=None) -> bool:
        """Validate the rule.
        """
        if self._value:
            self._validation_state = True
        else:
            msg_id = self._msg_id if self._msg_id else 'pytsite.core@validation_rule_not_empty'
            self._message = t(msg_id, {'name': field_name})
            self._validation_state = False

        return self._validation_state


class IntegerRule(BaseRule):
    """Integer rule.
    """

    def validate(self, validator=None, field_name: str=None) -> bool:
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


class UrlRule(BaseRule):
    """URL rule.
    """

    def validate(self, validator=None, field_name: str=None) -> bool:
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


class EmailRule(BaseRule):
    """Email rule.
    """

    def validate(self, validator=None, field_name: str=None) -> bool:
        """Validate the rule.
        """

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
