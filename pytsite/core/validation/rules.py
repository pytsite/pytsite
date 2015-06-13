"""Basic Validation Rules.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import re
from datetime import datetime
from abc import ABC, abstractmethod
from pytsite.core.lang import t
from .errors import ValidationError


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
    def message(self) -> str:
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

    def validate(self, validator=None, field_name: str=None) -> bool:
        """Validate the rule.
        """
        try:
            self._do_validate(validator, field_name)
            self._validation_state = True
        except ValidationError as e:
            msg_id = self._msg_id if self._msg_id else 'pytsite.core.validation@validation_' + self.__class__.__name__.lower()
            self._message = t(msg_id, {'field_name': field_name, 'error_detail': str(e)})
            self._validation_state = False

        return self._validation_state

    @abstractmethod
    def _do_validate(self, validator=None, field_name: str=None) -> bool:
        """Do actual validation of the rule.
        """
        pass


class NotEmptyRule(BaseRule):
    """Not empty rule.
    """

    def _do_validate(self, validator=None, field_name: str=None):
        """Do actual validation of the rule.
        """
        if isinstance(self.value, dict):
            empty = True
            for v in self.value.values():
                if v:
                    empty = False
                    break
            if empty:
                raise ValidationError()
        elif not self._value:
            raise ValidationError()


class DictValueNotEmptyRule(BaseRule):
    """Check if a dict value is empty.
    """

    def __init__(self, msg_id: str=None, value=None, keys: tuple=()):
        """Init.
        """
        super().__init__(msg_id, value)
        self._keys = keys

    def _do_validate(self, validator=None, field_name: str=None):
        """Do actual validation of the rule.
        """
        if not isinstance(self._value, dict):
            raise ValidationError('Value is not a dict.')

        if not self._keys:
            return

        for k in self._keys:
            if k in self._value and not self._value[k]:
                raise ValidationError()


class IntegerRule(BaseRule):
    """Integer rule.
    """

    def _do_validate(self, validator=None, field_name: str=None):
        """Do actual validation of the rule.
        """
        try:
            int(self._value)
        except ValueError:
            raise ValidationError()


class UrlRule(BaseRule):
    """URL rule.
    """

    def _do_validate(self, validator=None, field_name: str=None):
        """Do actual validation of the rule.
        """

        regex = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        if not regex.match(str(self._value)):
            raise ValidationError()


class EmailRule(BaseRule):
    """Email rule.
    """

    def _do_validate(self, validator=None, field_name: str=None):
        """Do actual validation of the rule.
        """
        regex = re.compile('[^@]+@[^@]+\.[^@]+')
        if not regex.match(str(self._value)):
            raise ValidationError()


class DateTimeRule(BaseRule):
    """Date/time Rule.
    """
    def _do_validate(self, validator=None, field_name: str=None):
        """Do actual validation of the rule.
        """
        if isinstance(self._value, str):
            if not re.match(r'\d{2}\.\d{2}\.\d{4}\s\d{2}\.\d{2}', self._value):
                raise ValidationError()
        elif not isinstance(self._value, datetime):
            raise ValidationError()
